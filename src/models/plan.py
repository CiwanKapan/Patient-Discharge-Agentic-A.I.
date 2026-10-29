"""Recommendations, approval classifications, and the final discharge plan.

    05 Rec. Generator  -> RecommendationSet   ranked next steps, LLM output
    06 Approval Gate   -> ApprovalDecisions   deterministic safety tag per recommendation
    08 Output Composer -> DischargePlan       the plan the system produced, in one object
    09 Sign-off request -> SignoffRequest     the plan's status and the actions awaiting a clinician

The agent may propose an approval-required action (GR-A*) but never execute it.
Such a recommendation must be classified ``requires_human_approval``; anything
else is a governance failure. Some tasks need such an action to be completed at
all (the taxonomy's ``governance.task_approvals``), so a recommendation for one
of them needs approval even when the model left ``proposed_action`` empty.
``check_governance`` enforces both against the taxonomy.
"""
from __future__ import annotations

from typing import ClassVar, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from src.models.messages import (
    AgentMessage,
    BarrierFinding,
    InformationGap,
    OwnerRole,
    Stage,
    TaskFinding,
    Urgency,
)
from src.models.tools import PolicyDecision, ToolCall


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


# ------------------------------------------------------------------ 05 Rec. Generator
class Recommendation(_Strict):
    recommendation_id: str
    rank: int = Field(
        ge=1,
        description="1 is the most urgent. Equally urgent recommendations share a rank "
        "(dense ranking: 1, 1, 2 is valid; 1, 1, 3 is not).",
    )
    kind: Literal["complete_task", "verify_information"] = Field(
        description="complete_task resolves a flagged barrier; "
        "verify_information asks a human to confirm an information gap."
    )
    description: str
    urgency: Urgency
    owner_role: OwnerRole
    task_id: Optional[str] = Field(None, pattern=r"^T-(MD|RN|PH|CM)\d{2}$")
    barrier_ids: list[str] = Field(default_factory=list)
    information_gap_field: Optional[str] = None
    proposed_action: Optional[str] = Field(
        None,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="Action name the agent wants taken, e.g. 'escalate_to_attending_physician'. "
        "Matched against the taxonomy by the approval gate.",
    )
    proposed_tool_calls: list[ToolCall] = Field(default_factory=list)

    @model_validator(mode="after")
    def _kind_fields(self) -> "Recommendation":
        if self.kind == "complete_task":
            if not self.task_id or not self.barrier_ids:
                raise ValueError("complete_task needs a task_id and the barrier_ids it resolves")
            if self.information_gap_field:
                raise ValueError("complete_task must not reference an information gap")
        else:
            if not self.information_gap_field:
                raise ValueError("verify_information needs information_gap_field")
            if self.task_id or self.barrier_ids:
                raise ValueError("verify_information must not claim a task or barrier")
        return self


class RecommendationSet(_Strict):
    STAGE: ClassVar[Stage] = Stage.REC_GENERATOR

    recommendations: list[Recommendation] = Field(default_factory=list)

    @model_validator(mode="after")
    def _unique_ids_and_dense_ranks(self) -> "RecommendationSet":
        ids = [r.recommendation_id for r in self.recommendations]
        if len(ids) != len(set(ids)):
            raise ValueError("recommendation_id values must be unique")
        distinct = sorted({r.rank for r in self.recommendations})
        if distinct != list(range(1, len(distinct) + 1)):
            raise ValueError("ranks must start at 1 and skip no numbers; ties are allowed (e.g. 1, 1, 2)")
        return self


# ------------------------------------------------------------------ 06 Approval Gate
Classification = Literal["auto_safe", "requires_human_approval", "forbidden"]


class ApprovalClassification(_Strict):
    recommendation_id: str
    classification: Classification
    requires_human_approval: bool
    matched_rule_id: Optional[str] = Field(
        None,
        pattern=r"^(GR-A|GF-T|GA-T)\d{2}$",
        description="GR-A* for approval-required actions, GF-T* for forbidden tools.",
    )
    reason: str
    label_missing: bool = Field(
        False,
        description="True when approval comes from the task (governance.task_approvals) because the "
        "recommendation named no approval-required action. Records the model's omission.",
    )

    @model_validator(mode="after")
    def _consistent(self) -> "ApprovalClassification":
        if self.requires_human_approval != (self.classification == "requires_human_approval"):
            raise ValueError("requires_human_approval must be true exactly when classification says so")
        rule = self.matched_rule_id or ""
        if self.classification == "requires_human_approval" and not rule.startswith("GR-A"):
            raise ValueError("requires_human_approval must cite a GR-A* rule")
        if self.classification == "forbidden" and not rule.startswith("GF-T"):
            raise ValueError("forbidden must cite a GF-T* rule")
        if self.label_missing and self.classification != "requires_human_approval":
            raise ValueError("label_missing applies only to requires_human_approval")
        return self


class ApprovalDecisions(_Strict):
    STAGE: ClassVar[Stage] = Stage.APPROVAL_GATE

    classifications: list[ApprovalClassification] = Field(default_factory=list)

    @model_validator(mode="after")
    def _one_per_recommendation(self) -> "ApprovalDecisions":
        ids = [c.recommendation_id for c in self.classifications]
        if len(ids) != len(set(ids)):
            raise ValueError("each recommendation gets exactly one classification")
        return self


# ------------------------------------------------------------------ 08 Output Composer
class PlannedAction(_Strict):
    recommendation: Recommendation
    approval: ApprovalClassification

    @model_validator(mode="after")
    def _same_recommendation(self) -> "PlannedAction":
        if self.recommendation.recommendation_id != self.approval.recommendation_id:
            raise ValueError("approval belongs to a different recommendation")
        return self


PlanStatus = Literal["pending_clinician_signoff", "final"]
PENDING: PlanStatus = "pending_clinician_signoff"


class DischargePlan(_Strict):
    """The structured plan a run returns (logged as AU-07)."""

    STAGE: ClassVar[Stage] = Stage.OUTPUT_COMPOSER

    case_id: str
    status: PlanStatus = Field(
        PENDING,
        description="Every plan is emitted pending_clinician_signoff: the system only proposes, and a clinician "
        "signs off outside it. A plan marked final is a governance failure (check_plan_status).",
    )
    summary: str
    barriers: list[BarrierFinding] = Field(default_factory=list)
    information_gaps: list[InformationGap] = Field(default_factory=list)
    tasks: list[TaskFinding] = Field(default_factory=list)
    actions: list[PlannedAction] = Field(default_factory=list, description="In rank order.")
    denied_tool_calls: list[PolicyDecision] = Field(default_factory=list)
    unaddressed_barriers: list[str] = Field(
        default_factory=list,
        description="Flagged barriers that no task resolves. Derived from barriers and tasks; "
        "any value passed in is replaced.",
    )

    @model_validator(mode="after")
    def _ordered_and_denied_only(self) -> "DischargePlan":
        resolved = {b for t in self.tasks for b in t.resolves}
        self.unaddressed_barriers = [b.barrier_id for b in self.barriers if b.barrier_id not in resolved]
        ranks = [a.recommendation.rank for a in self.actions]
        if ranks != sorted(ranks):
            raise ValueError("actions must be listed in rank order")
        if any(d.decision != "denied" for d in self.denied_tool_calls):
            raise ValueError("denied_tool_calls may only hold denied decisions")
        return self


# ------------------------------------------------------------------ 09 Sign-off request
class SignoffItem(_Strict):
    """One action the approval gate marked requires_human_approval, awaiting a clinician."""

    recommendation_id: str
    task_id: Optional[str] = None
    matched_rule_id: str = Field(pattern=r"^GR-A\d{2}$", description="The approval rule the clinician signs off.")


class SignoffRequest(_Strict):
    """Logged as AU-09 (signoff_requested) when the plan is emitted. The system never
    records a clinician's decision; it only requests one."""

    STAGE: ClassVar[Stage] = Stage.SIGNOFF_REQUEST

    status: PlanStatus = PENDING
    actions: list[SignoffItem] = Field(default_factory=list, description="Gated actions awaiting sign-off.")

    @model_validator(mode="after")
    def _one_per_action(self) -> "SignoffRequest":
        ids = [a.recommendation_id for a in self.actions]
        if len(ids) != len(set(ids)):
            raise ValueError("one sign-off item per recommendation")
        return self


def signoff_request(plan: DischargePlan) -> SignoffRequest:
    """The request for ``plan``: its status and every gated action."""
    return SignoffRequest(status=plan.status, actions=[
        SignoffItem(recommendation_id=a.recommendation.recommendation_id, task_id=a.recommendation.task_id,
                    matched_rule_id=a.approval.matched_rule_id)
        for a in gated_actions(plan)])


def check_plan_status(plan: DischargePlan) -> list[str]:
    """A plan must be emitted pending clinician sign-off; one marked final is a governance failure."""
    if plan.status != PENDING:
        return [f"plan marked {plan.status}; it must be emitted {PENDING}"]
    return []


def gated_actions(plan: DischargePlan) -> list[PlannedAction]:
    """The plan's actions that need human sign-off before anything is done."""
    return [a for a in plan.actions if a.approval.requires_human_approval]


# ------------------------------------------------------------------ governance check
def task_approval(taxonomy: dict, task_id: Optional[str]) -> Optional[dict]:
    """The approval-required action (GR-A* entry) that completing ``task_id`` needs, if any."""
    gov = taxonomy["governance"]
    rule_id = gov.get("task_approvals", {}).get(task_id or "")
    return next((a for a in gov["approval_required_actions"] if a["id"] == rule_id), None)


def check_governance(
    taxonomy: dict, recommendations: RecommendationSet, approvals: ApprovalDecisions
) -> list[str]:
    """Check approval classifications against the taxonomy (empty list = OK).

    - every recommendation is classified exactly once
    - a recommendation that would call a GF-T* tool is classified forbidden
    - otherwise a GR-A* action is classified requires_human_approval with that rule
    - otherwise a task that needs approval (governance.task_approvals) is classified
      requires_human_approval with the task's rule, even with no proposed_action

    Some names are both a GR-A* action and a GF-T* tool (e.g. modify_medication_list).
    Proposing the action for a human is allowed with approval; calling the tool is not.
    - auto_safe is used only when nothing proposed is approval-required or forbidden
    """
    gov = taxonomy["governance"]
    gr = {a["action"]: a["id"] for a in gov["approval_required_actions"]}
    gf = {t["tool_name"]: t["id"] for t in gov["forbidden_tools"]}
    by_id = {c.recommendation_id: c for c in approvals.classifications}
    errors = []

    known = {r.recommendation_id for r in recommendations.recommendations}
    for extra in sorted(set(by_id) - known):
        errors.append(f"classification for unknown recommendation {extra}")

    for r in recommendations.recommendations:
        c = by_id.get(r.recommendation_id)
        if c is None:
            errors.append(f"{r.recommendation_id} was not classified")
            continue
        forbidden = sorted(gf[t.tool_name] for t in r.proposed_tool_calls if t.tool_name in gf)
        if r.proposed_action in gf and r.proposed_action not in gr:
            forbidden.append(gf[r.proposed_action])
        if forbidden:
            if c.classification != "forbidden" or c.matched_rule_id not in forbidden:
                errors.append(f"{r.recommendation_id} proposes forbidden {forbidden} but is {c.classification}")
        elif r.proposed_action in gr:
            if c.classification != "requires_human_approval" or c.matched_rule_id != gr[r.proposed_action]:
                errors.append(
                    f"{r.recommendation_id} proposes {r.proposed_action} ({gr[r.proposed_action]}) "
                    f"but is {c.classification}/{c.matched_rule_id}"
                )
        elif (needed := task_approval(taxonomy, r.task_id)) is not None:
            if c.classification != "requires_human_approval" or c.matched_rule_id != needed["id"]:
                errors.append(
                    f"{r.recommendation_id} is task {r.task_id}, which needs {needed['action']} "
                    f"({needed['id']}), but is {c.classification}/{c.matched_rule_id}"
                )
        elif c.classification == "forbidden":
            errors.append(f"{r.recommendation_id} classified forbidden with no forbidden tool or action")
    return errors


RecommendationMessage = AgentMessage[RecommendationSet]
SignoffMessage = AgentMessage[SignoffRequest]
ApprovalMessage = AgentMessage[ApprovalDecisions]
DischargePlanMessage = AgentMessage[DischargePlan]
