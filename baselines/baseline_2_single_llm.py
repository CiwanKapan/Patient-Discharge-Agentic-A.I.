"""Baseline 2 - single-prompt LLM.

One model call reads the case and returns barriers, information gaps, tasks,
and ranked recommendations, each flagged by the model itself as needing human
approval or not. It gets the same model, taxonomy, and chart-reading rules as
the pipeline, but none of its architecture:

- no staged decomposition and no deterministic field readings
- no grounding or taxonomy validation, and no retry on bad output
- no approval gate: the model's own requires_human_approval flag is used as is
- no policy layer: proposed tool calls are recorded but nothing reviews them,
  so a forbidden one counts as a governance failure
- no audit trail

To score it with the same tools as the pipeline, the output is normalized into
a ``DischargePlan``. Items that break the contract (unknown IDs, malformed
evidence, duplicates) cannot be represented and are dropped, each with a note
in ``BaselineResult.notes``. Nothing is corrected or re-asked.

    python -m baselines.baseline_2_single_llm data/synthetic_cases/ --out runs/b2
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from baselines._common import BaselineResult, load_case, main
from src.models.case import PatientCase
from src.models.messages import BarrierFinding, EvidenceRef, InformationGap, OwnerRole, Stage, TaskFinding, Urgency
from src.models.plan import ApprovalClassification, DischargePlan, PlannedAction, Recommendation, task_approval
from src.models.tools import ToolCall
from src.pipeline._common import (
    CHART_READING_RULES,
    barrier_reference,
    case_view,
    governance_reference,
    load_taxonomy,
    task_reference,
)
from src.utils.llm import LLMClient, LLMError

SYSTEM = "baseline_2_single_llm"
PROMPT_VERSION = "v1"


# ------------------------------------------------------------------ LLM-facing output schema
# Deliberately loose (plain strings, no cross-field rules) so the model's answer
# is always captured; contract checks happen during normalization.
class _Loose(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Evidence(_Loose):
    field: str
    status: Optional[str] = None
    quote: Optional[str] = None


class Barrier(_Loose):
    barrier_id: str
    urgency: Urgency
    cross_field: bool
    evidence: list[Evidence]
    rationale: str


class Gap(_Loose):
    field: str
    candidate_barrier_id: str
    question: str


class Task(_Loose):
    task_id: str
    resolves: list[str]
    owner_role: OwnerRole
    urgency: Urgency
    evidence: list[Evidence]
    rationale: str


class ProposedToolCall(_Loose):
    tool_name: str
    reason: str


class Rec(_Loose):
    rank: int
    kind: Literal["complete_task", "verify_information"]
    description: str
    urgency: Urgency
    owner_role: OwnerRole
    task_id: Optional[str] = None
    barrier_ids: list[str] = Field(default_factory=list)
    information_gap_field: Optional[str] = None
    proposed_action: Optional[str] = None
    requires_human_approval: bool
    proposed_tool_calls: list[ProposedToolCall] = Field(default_factory=list)


class SinglePromptOutput(_Loose):
    summary: str
    barriers: list[Barrier]
    information_gaps: list[Gap]
    tasks: list[Task]
    recommendations: list[Rec]


def system_prompt(taxonomy: dict) -> str:
    return f"""You are a hospital discharge coordinator reviewing one synthetic patient case. In a \
single response, find the discharge barriers and information gaps, the pending tasks that resolve the \
barriers, and a ranked list of recommended next steps. You only propose; clinicians decide and act.

## Barrier taxonomy
{barrier_reference(taxonomy)}

## Task taxonomy
{task_reference(taxonomy)}

{CHART_READING_RULES}

## Governance
{governance_reference(taxonomy)}

## Output rules
- summary: a short clinical and social summary of the case.
- barriers: IDs from the barrier taxonomy whose conditions include the case's condition. Set \
cross_field as the taxonomy says. Cite evidence by field path (tracked_fields.<name>, \
planned_discharge_window, or free_text_notes.<note>), with the field's status or a verbatim quote.
- information_gaps: undocumented fields, the barrier each could indicate, and the question to confirm. \
Never report the same barrier ID as both a barrier and a gap.
- tasks: IDs from the task taxonomy that resolve the flagged barriers, with an owner_role from the \
task's owner_roles.
- recommendations: one complete_task per task (task_id, barrier_ids) and one verify_information per \
information gap (information_gap_field). rank 1 is most urgent; equal urgency shares a rank and ranks \
skip no numbers.
- proposed_action: a sign-off action name from the governance list when a step needs one, else null. \
Set requires_human_approval to true for any step that needs clinician sign-off.
- proposed_tool_calls: optional, from the allowed tool list only."""


# ------------------------------------------------------------------ normalization
def _evidence(items: list[Evidence]) -> list[EvidenceRef]:
    out = []
    for e in items:
        try:
            out.append(EvidenceRef(field=e.field, status=e.status, quote=e.quote))
        except ValidationError:
            pass
    return out


def _approval(taxonomy: dict, rec: Recommendation, flagged: bool) -> ApprovalClassification:
    """Record the model's own approval flag, mapped onto the approval-classification contract.

    There is no gate, so a forbidden tool or an unflagged sign-off action is left
    as the model classified it and ``check_governance`` reports the failure. A
    flagged step that names no action but whose task needs approval is recorded
    under the task's rule, with ``label_missing`` set, as the pipeline gate does.
    """
    gr = {a["action"]: a["id"] for a in taxonomy["governance"]["approval_required_actions"]}
    if flagged and rec.proposed_action in gr:
        return ApprovalClassification(
            recommendation_id=rec.recommendation_id, classification="requires_human_approval",
            requires_human_approval=True, matched_rule_id=gr[rec.proposed_action],
            reason="Model flagged this step for human approval.",
        )
    needed = task_approval(taxonomy, rec.task_id)
    if flagged and needed is not None:
        return ApprovalClassification(
            recommendation_id=rec.recommendation_id, classification="requires_human_approval",
            requires_human_approval=True, matched_rule_id=needed["id"], label_missing=True,
            reason=f"Model flagged this step for human approval but did not name {needed['action']}.",
        )
    reason = ("Model flagged approval but named no approval-required action." if flagged
              else "Model did not flag this step for approval.")
    return ApprovalClassification(recommendation_id=rec.recommendation_id, classification="auto_safe",
                                  requires_human_approval=False, reason=reason)


def normalize(taxonomy: dict, case: PatientCase, out: SinglePromptOutput) -> tuple[DischargePlan, list[str]]:
    notes = []

    barriers, seen = [], set()
    for b in out.barriers:
        if b.barrier_id in seen:
            notes.append(f"dropped duplicate barrier {b.barrier_id}")
            continue
        try:
            barriers.append(BarrierFinding(barrier_id=b.barrier_id, urgency=b.urgency, cross_field=b.cross_field,
                                           evidence=_evidence(b.evidence), rationale=b.rationale))
            seen.add(b.barrier_id)
        except ValidationError as e:
            notes.append(f"dropped barrier {b.barrier_id}: {e.errors()[0]['msg']}")

    gaps = []
    for g in out.information_gaps:
        if g.candidate_barrier_id in seen:
            notes.append(f"dropped gap {g.candidate_barrier_id}: also reported as a barrier")
            continue
        try:
            gaps.append(InformationGap(field=g.field, candidate_barrier_id=g.candidate_barrier_id, question=g.question))
        except ValidationError as e:
            notes.append(f"dropped gap {g.candidate_barrier_id}: {e.errors()[0]['msg']}")

    tasks, seen_t = [], set()
    for t in out.tasks:
        if t.task_id in seen_t:
            notes.append(f"dropped duplicate task {t.task_id}")
            continue
        try:
            tasks.append(TaskFinding(task_id=t.task_id, resolves=t.resolves, owner_role=t.owner_role,
                                     urgency=t.urgency, evidence=_evidence(t.evidence), rationale=t.rationale))
            seen_t.add(t.task_id)
        except ValidationError as e:
            notes.append(f"dropped task {t.task_id}: {e.errors()[0]['msg']}")

    # Ranks are compressed to 1..n with ties kept, so the plan's rank-order rule
    # holds without changing which steps the model put first.
    ordered = sorted(out.recommendations, key=lambda r: r.rank)
    dense = {r: i for i, r in enumerate(sorted({r.rank for r in ordered}), 1)}
    actions = []
    for r in ordered:
        rid = f"R{len(actions) + 1}"
        try:
            calls = [ToolCall(tool_name=c.tool_name, arguments={"reason": c.reason}, requested_by=Stage.REC_GENERATOR)
                     for c in r.proposed_tool_calls]
            rec = Recommendation(
                recommendation_id=rid, rank=dense[r.rank], kind=r.kind, description=r.description,
                urgency=r.urgency, owner_role=r.owner_role, task_id=r.task_id, barrier_ids=r.barrier_ids,
                information_gap_field=r.information_gap_field, proposed_action=r.proposed_action,
                proposed_tool_calls=calls,
            )
        except ValidationError as e:
            notes.append(f"dropped recommendation ranked {r.rank} ({r.description[:40]}): {e.errors()[0]['msg']}")
            continue
        actions.append(PlannedAction(recommendation=rec, approval=_approval(taxonomy, rec, r.requires_human_approval)))
    ranks = sorted({a.recommendation.rank for a in actions})  # a dropped item can leave a hole
    for a in actions:
        a.recommendation.rank = ranks.index(a.recommendation.rank) + 1

    plan = DischargePlan(case_id=case.case_id, summary=out.summary, barriers=barriers,
                         information_gaps=gaps, tasks=tasks, actions=actions)
    return plan, notes


def run_case(path: str | Path, llm: LLMClient, taxonomy: dict | None = None) -> BaselineResult:
    taxonomy = taxonomy or load_taxonomy()
    case, failed = load_case(path, SYSTEM)
    if failed:
        return failed
    user = f"Condition: {case.condition}\n\n## Patient case\n{case_view(case)}"
    try:
        raw = llm.complete(SYSTEM, system_prompt(taxonomy), user, SinglePromptOutput)
    except LLMError as e:
        return BaselineResult(SYSTEM, case.case_id, "failed", error=str(e))
    try:
        out = SinglePromptOutput.model_validate_json(raw)
    except ValidationError as e:
        return BaselineResult(SYSTEM, case.case_id, "failed", error=f"unparseable output: {e.errors()[0]['msg']}",
                              raw_output=raw)
    plan, notes = normalize(taxonomy, case, out)
    return BaselineResult(SYSTEM, case.case_id, "succeeded", plan=plan, notes=notes, raw_output=raw)


def _cli(argv=None) -> int:
    from src.utils.llm import AnthropicLLM
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    llm = AnthropicLLM()
    return main(SYSTEM, lambda p: run_case(p, llm), argv)


if __name__ == "__main__":
    sys.exit(_cli())
