"""Stage 09 - Sign-off (deterministic; the decisions come from a reviewer).

Runs after the output composer. Every action the approval gate marked
requires_human_approval gets one sign-off decision: approved, rejected, or
pending. Forbidden actions are never offered for sign-off; they cannot be
approved. Auto-safe actions need none.

The decisions are kept apart from the composed plan (AU-07), so scoring measures
what the system produced, not what a reviewer did with it. Each decision is
logged as AU-09. Nothing is carried out here, whatever the decision.

This is an offline benchmark with no clinician in the loop, so the reviewer is
pluggable:

    pending      (default) no one has reviewed the plan; every gated action
                 stays pending and must not be carried out
    approve_all  a simulated clinician approves every gated action
"""
from __future__ import annotations

from typing import Protocol

from src.models.messages import AgentMessage, Stage
from src.models.plan import DischargePlan, PlannedAction, SignoffDecision, SignoffDecisions, gated_actions
from src.pipeline._common import RunContext, StageError, make_message

STAGE = Stage.SIGNOFF


class Reviewer(Protocol):
    name: str

    def review(self, plan: DischargePlan, action: PlannedAction) -> tuple[str, str]:
        """Return (decision, reason) for one gated action; decision is approved, rejected, or pending."""
        ...


class PendingReviewer:
    name = "none"

    def review(self, plan, action):
        return "pending", "Awaiting clinician sign-off; not carried out until approved."


class ApproveAllReviewer:
    name = "simulated:approve_all"

    def review(self, plan, action):
        return "approved", f"Simulated clinician approved {action.approval.matched_rule_id}."


REVIEWERS = {"pending": PendingReviewer, "approve_all": ApproveAllReviewer}


def run(ctx: RunContext, plan: AgentMessage[DischargePlan], reviewer: Reviewer) -> AgentMessage[SignoffDecisions]:
    decisions = decide(plan.payload, reviewer)
    warnings = [] if decisions.decisions else ["no action needs sign-off"]
    return make_message(ctx, STAGE, decisions, [plan], warnings)


def decide(plan: DischargePlan, reviewer: Reviewer) -> SignoffDecisions:
    """One decision per gated action. Also used by B3."""
    decisions = []
    for a in gated_actions(plan):
        decision, reason = reviewer.review(plan, a)
        try:
            decisions.append(SignoffDecision(
                recommendation_id=a.recommendation.recommendation_id, task_id=a.recommendation.task_id,
                matched_rule_id=a.approval.matched_rule_id, decision=decision, reviewer=reviewer.name, reason=reason,
            ))
        except ValueError as e:
            raise StageError(STAGE, f"reviewer {reviewer.name} returned an invalid decision: {e}") from e
    return SignoffDecisions(decisions=decisions)
