"""Stage 08 - Output Composer (deterministic).

Assembles the final ``DischargePlan`` from the stage outputs: findings from
stages 03-04, each recommendation paired with its approval classification in
rank order, and every tool call the policy layer denied.
"""
from __future__ import annotations

from src.models.messages import AgentMessage, BarrierDetection, CaseSummary, Stage, TaskDetection
from src.models.plan import ApprovalDecisions, DischargePlan, PlannedAction, RecommendationSet
from src.models.tools import PolicyLayerOutput
from src.pipeline._common import RunContext, make_message

STAGE = Stage.OUTPUT_COMPOSER


def run(
    ctx: RunContext,
    summary: AgentMessage[CaseSummary],
    barriers: AgentMessage[BarrierDetection],
    tasks: AgentMessage[TaskDetection],
    recs: AgentMessage[RecommendationSet],
    approvals: AgentMessage[ApprovalDecisions],
    policy: AgentMessage[PolicyLayerOutput],
) -> AgentMessage[DischargePlan]:
    plan = compose(ctx.case_id, f"{summary.payload.clinical_summary}\n\n{summary.payload.social_summary}",
                   barriers.payload, tasks.payload, recs.payload, approvals.payload, policy.payload)
    return make_message(ctx, STAGE, plan, [summary, barriers, tasks, recs, approvals, policy])


def compose(case_id: str, summary: str, barriers: BarrierDetection, tasks: TaskDetection, recs: RecommendationSet,
            approvals: ApprovalDecisions, policy: PolicyLayerOutput) -> DischargePlan:
    """The plan from stage payloads. Also used by B3, which reaches these payloads in one model call."""
    by_id = {c.recommendation_id: c for c in approvals.classifications}
    ordered = sorted(recs.recommendations, key=lambda r: r.rank)  # stable: ties keep list order
    return DischargePlan(
        case_id=case_id,
        summary=summary,
        barriers=barriers.barriers,
        information_gaps=barriers.information_gaps,
        tasks=tasks.tasks,
        actions=[PlannedAction(recommendation=r, approval=by_id[r.recommendation_id]) for r in ordered],
        denied_tool_calls=[d for d in policy.decisions if d.decision == "denied"],
    )
