"""Stage 09 - Sign-off request (deterministic).

Runs when the output composer emits the plan. The system only proposes; a
clinician signs off outside it. So every plan is emitted with status
pending_clinician_signoff, and this stage requests sign-off: it lists every
action the approval gate marked requires_human_approval (forbidden actions are
never offered; auto-safe ones need none). The request is logged as AU-09
(signoff_requested) right after output_emitted (AU-07).

The system never records a clinician's decision and never marks a plan final;
a plan marked final is a governance failure (check_plan_status).
"""
from __future__ import annotations

from src.models.messages import AgentMessage, Stage
from src.models.plan import DischargePlan, SignoffRequest, signoff_request
from src.pipeline._common import RunContext, make_message

STAGE = Stage.SIGNOFF_REQUEST


def run(ctx: RunContext, plan: AgentMessage[DischargePlan]) -> AgentMessage[SignoffRequest]:
    request = signoff_request(plan.payload)
    warnings = [] if request.actions else ["no action needs clinician approval; the plan still awaits sign-off"]
    return make_message(ctx, STAGE, request, [plan], warnings)
