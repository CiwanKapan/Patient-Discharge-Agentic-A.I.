"""Baseline 3 (B2+scaffold) - one model call wrapped in the pipeline's deterministic code.

A pre-registered secondary arm. It asks whether the agentic pipeline's gains
come from multi-stage decomposition or from the deterministic code around the
model. B3 is B2 plus every deterministic part of the pipeline, and nothing else:

    input   B2's system prompt and case, plus what the pipeline computes in code
            and shows its models: a reading per tracked field (complete / not done /
            undocumented) and the documented time windows. Nothing more: the
            pipeline never shows its models a transport-timing verdict, so B3
            does not get one either.
    output  B2's output schema, normalized as in B2 (contract-breaking items are
            dropped, never corrected), then run through the pipeline's approval
            gate (stage 06), policy layer (07), output composer (08), sign-off (09),
            and audit trail. The model's own approval flags are ignored; the gate decides.

What B3 lacks compared with the pipeline: the case analyzer's LLM summary, separate
calls per stage, and the per-stage taxonomy and evidence validation with its
retries. Like B2 it retries format failures only (baselines/_single_prompt.py).

Model, effort, max_tokens, and attempts come from config/run_config.json.

    python -m baselines.baseline_3_scaffold data/synthetic_cases/ --out runs/b3 [--batch]
"""
from __future__ import annotations

import importlib
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from baselines import baseline_2_single_llm as b2
from baselines._common import BaselineResult, main
from baselines._single_prompt import Answer, ask, ask_batch
from src.models.audit import (
    ApprovalClassificationDetails,
    ApprovalClassified,
    BarrierFlagged,
    BarrierFlaggedDetails,
    CaseLoaded,
    OutputEmitted,
    OutputEmittedDetails,
    PolicyDecisionDetails,
    PolicyDecisionEvent,
    RunCompleted,
    RunCompletedDetails,
    SignoffRecorded,
    TaskRecommended,
    TaskRecommendedDetails,
    ToolCallDetails,
    ToolCallEvent,
    check_audit_trail,
)
from src.models.case import PatientCase
from src.models.messages import BarrierDetection, Stage, TaskDetection
from src.models.plan import ApprovalDecisions, RecommendationSet, check_governance
from src.models.tools import check_policy
from src.pipeline._common import RunContext, StageError, case_view, load_taxonomy, snapshot_lines
from src.utils.audit_logger import AuditLogger, read_audit_log
from src.utils.case_checks import snapshot_fields, time_constraints
from src.utils.run_config import check_environment, load_run_config

input_reader = importlib.import_module("src.pipeline.01_input_reader")
approval_gate = importlib.import_module("src.pipeline.06_approval_gate")
policy_layer = importlib.import_module("src.pipeline.07_policy_layer")
output_composer = importlib.import_module("src.pipeline.08_output_composer")
signoff = importlib.import_module("src.pipeline.09_signoff")

SYSTEM = "baseline_3_scaffold"
PROMPT_VERSION = "v1"
DEFAULT_AUDIT_DIR = Path("runs") / "audit_b3"


def user_prompt(case: PatientCase) -> str:
    """B2's input plus the deterministic readings the pipeline shows its models."""
    windows = "\n".join(f"- {w.field}: {w.window.start.isoformat()} to {w.window.end.isoformat()}"
                        for w in time_constraints(case)) or "- none documented"
    return (
        f"Condition: {case.condition}\n\n## Patient case\n{case_view(case)}\n\n"
        f"## Field readings (computed from status)\n{snapshot_lines(snapshot_fields(case))}\n\n"
        f"## Time windows\n{windows}"
    )


def finish(taxonomy: dict, loaded, answer: Optional[Answer], audit_dir: Path, reviewer,
           model: str, llm_settings: Optional[dict] = None) -> BaselineResult:
    """Normalize the answer, run the governance code, and write the audit trail."""
    run_id = uuid.uuid4().hex
    started = datetime.now(timezone.utc)
    audit_path = Path(audit_dir) / loaded.case_id / f"{run_id}.jsonl"
    r = BaselineResult(SYSTEM, loaded.case_id, "failed", audit_path=audit_path, llm_settings=llm_settings)
    if answer is not None:
        r.raw_output, r.llm_calls = answer.raw, answer.calls
    tool_calls = 0
    with AuditLogger(audit_path, run_id, loaded.case_id) as log:
        log.log(CaseLoaded, loaded.details, stage=Stage.INPUT_READER)
        try:
            if loaded.case is None:
                raise StageError(Stage.INPUT_READER, loaded.error)
            if answer.out is None:
                r.error, r.error_kind = answer.error, answer.error_kind
            else:
                draft, r.notes = b2.normalize(taxonomy, loaded.case, answer.out)
                barriers = BarrierDetection(barriers=draft.barriers, information_gaps=draft.information_gaps)
                tasks = TaskDetection(tasks=draft.tasks)
                recs = RecommendationSet(recommendations=[a.recommendation for a in draft.actions])
                for b in barriers.barriers:
                    log.log(BarrierFlagged, BarrierFlaggedDetails(
                        barrier_id=b.barrier_id, evidence_fields=list(dict.fromkeys(e.field for e in b.evidence)),
                        urgency=b.urgency))
                for t in tasks.tasks:
                    log.log(TaskRecommended, TaskRecommendedDetails(
                        task_id=t.task_id, owner_role=t.owner_role, linked_barrier_ids=t.resolves))

                approvals = ApprovalDecisions(classifications=[approval_gate.classify(taxonomy, x)
                                                               for x in recs.recommendations])
                for c in approvals.classifications:
                    log.log(ApprovalClassified, ApprovalClassificationDetails(**c.model_dump()), Stage.APPROVAL_GATE)
                errors = check_governance(taxonomy, recs, approvals)
                if errors:
                    raise StageError(Stage.APPROVAL_GATE, "governance check failed: " + "; ".join(errors))

                ctx = RunContext(run_id, loaded.case, taxonomy)
                calls = policy_layer.proposed_calls(recs)
                policy = policy_layer.review(ctx, calls)
                by_id, results = {c.call_id: c for c in calls}, {x.call_id: x for x in policy.results}
                for d in policy.decisions:
                    res = results.get(d.call_id)
                    log.log(ToolCallEvent, ToolCallDetails(call=by_id[d.call_id], decision=d.decision,
                                                           output=res.output if res else None,
                                                           error=res.error if res else None), Stage.POLICY_LAYER)
                    log.log(PolicyDecisionEvent, PolicyDecisionDetails(**d.model_dump()), Stage.POLICY_LAYER)
                    tool_calls += 1
                errors = check_policy(taxonomy, policy)
                if errors:
                    raise StageError(Stage.POLICY_LAYER, "policy check failed: " + "; ".join(errors))

                plan = output_composer.compose(loaded.case_id, answer.out.summary, barriers, tasks, recs,
                                               approvals, policy)
                log.log(OutputEmitted, OutputEmittedDetails(plan=plan), Stage.OUTPUT_COMPOSER)
                decided = signoff.decide(plan, reviewer)
                for d in decided.decisions:
                    log.log(SignoffRecorded, d, Stage.SIGNOFF)
                r.plan, r.signoffs, r.status = plan, decided.decisions, "succeeded"
        except StageError as e:
            r.error, r.error_kind = str(e), "output"
        log.log(RunCompleted, RunCompletedDetails(
            status=r.status, model=model, prompt_versions={SYSTEM: PROMPT_VERSION}, started_at=started,
            completed_at=datetime.now(timezone.utc), tool_call_count=tool_calls, error=r.error,
            llm_calls=r.llm_calls, llm_settings=llm_settings,
        ))
    r.audit_errors = check_audit_trail(read_audit_log(audit_path))
    return r


def run_case(path: str | Path, llm, taxonomy: dict | None = None, max_attempts: int = 2,
             audit_dir: Path = DEFAULT_AUDIT_DIR, reviewer=None, llm_settings: Optional[dict] = None) -> BaselineResult:
    taxonomy = taxonomy or load_taxonomy()
    loaded = input_reader.read_case(path)
    answer = None
    if loaded.case is not None:
        answer = ask(llm, SYSTEM, b2.system_prompt(taxonomy), user_prompt(loaded.case), b2.SinglePromptOutput,
                     max_attempts)
    return finish(taxonomy, loaded, answer, audit_dir, reviewer or signoff.PendingReviewer(), llm.model, llm_settings)


def run_cases_batch(paths: list[Path], llm, taxonomy: dict | None = None, max_attempts: int = 2,
                    audit_dir: Path = DEFAULT_AUDIT_DIR, reviewer=None, llm_settings: Optional[dict] = None,
                    **batch_kw) -> list[BaselineResult]:
    taxonomy = taxonomy or load_taxonomy()
    loaded = [input_reader.read_case(p) for p in paths]
    system = b2.system_prompt(taxonomy)
    prompts = {x.case_id: (system, user_prompt(x.case)) for x in loaded if x.case is not None}
    answers = ask_batch(llm, SYSTEM, prompts, b2.SinglePromptOutput, max_attempts, **batch_kw)
    reviewer = reviewer or signoff.PendingReviewer()
    return [finish(taxonomy, x, answers.get(x.case_id), audit_dir, reviewer, llm.model, llm_settings) for x in loaded]


def _cli(argv=None) -> int:
    from src.utils.llm import AnthropicLLM
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    settings = load_run_config().llm
    check_environment(settings)
    llm = AnthropicLLM.from_settings(settings)
    taxonomy = load_taxonomy()
    s = settings.model_dump()

    def add_args(p):
        p.add_argument("--audit-dir", type=Path, help="audit logs (default: <out>/audit, or runs/audit_b3)")
        p.add_argument("--signoff", default="pending", choices=sorted(signoff.REVIEWERS))

    def bind(args):
        audit = args.audit_dir or (args.out / "audit" if args.out else DEFAULT_AUDIT_DIR)
        reviewer = signoff.REVIEWERS[args.signoff]()
        kw = dict(taxonomy=taxonomy, max_attempts=settings.max_attempts, audit_dir=audit, reviewer=reviewer,
                  llm_settings=s)
        return (lambda p: run_case(p, llm, **kw)), (lambda ps: run_cases_batch(ps, llm, **kw))

    return main(SYSTEM, None, argv, batch=True, add_args=add_args, bind=bind, llm_settings=s,
                prompt_version=PROMPT_VERSION)


if __name__ == "__main__":
    sys.exit(_cli())
