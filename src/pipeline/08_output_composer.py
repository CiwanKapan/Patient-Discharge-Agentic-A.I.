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
    by_id = {c.recommendation_id: c for c in approvals.payload.classifications}
    ordered = sorted(recs.payload.recommendations, key=lambda r: r.rank)  # stable: ties keep list order
    plan = DischargePlan(
        case_id=ctx.case_id,
        summary=f"{summary.payload.clinical_summary}\n\n{summary.payload.social_summary}",
        barriers=barriers.payload.barriers,
        information_gaps=barriers.payload.information_gaps,
        tasks=tasks.payload.tasks,
        actions=[PlannedAction(recommendation=r, approval=by_id[r.recommendation_id]) for r in ordered],
        denied_tool_calls=[d for d in policy.payload.decisions if d.decision == "denied"],
    )
    return make_message(ctx, STAGE, plan, [summary, barriers, tasks, recs, approvals, policy])
