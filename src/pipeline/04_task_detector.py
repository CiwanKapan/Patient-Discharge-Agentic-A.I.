"""Stage 04 - Task Detector (LLM).

Maps each flagged barrier to the pending tasks that would resolve it. A task
must come from the taxonomy, fit the case's condition, be owned by one of its
listed roles, and resolve only barriers that stage 03 actually flagged.
"""
from __future__ import annotations

from src.models.messages import (
    AgentMessage,
    BarrierDetection,
    CaseSummary,
    Stage,
    TaskDetection,
    check_against_taxonomy,
)
from src.pipeline._common import (
    Rejected,
    RunContext,
    call_llm,
    case_view,
    check_evidence,
    make_message,
    task_reference,
)

STAGE = Stage.TASK_DETECTOR


def system_prompt(taxonomy: dict) -> str:
    return f"""You are the task detector in a supervised hospital discharge-coordination pipeline. \
Earlier stages have flagged the discharge barriers for a synthetic patient case. You decide which \
pending tasks from the closed taxonomy below would resolve them.

## Task taxonomy
{task_reference(taxonomy)}

## Output rules
- Recommend tasks only for barriers in the flagged list. Information gaps are not barriers; do not \
create tasks for them.
- Each task's resolves list names only flagged barriers that the taxonomy says the task can resolve.
- Use only tasks whose conditions include the case's condition.
- Pick the single most direct task for each barrier. Add a second task for the same barrier only when \
the chart shows that both are pending.
- owner_role must be one of the task's owner_roles.
- Every task cites evidence from the chart: the field path (tracked_fields.<name>, \
planned_discharge_window, or free_text_notes.<note>), the field's status when citing a tracked field, \
and a verbatim quote when citing a note.
- Use the taxonomy urgency unless the barrier's urgency is clearly higher."""


def run(
    ctx: RunContext, summary: AgentMessage[CaseSummary], barriers: AgentMessage[BarrierDetection]
) -> AgentMessage[TaskDetection]:
    flagged = barriers.payload.model_dump_json(include={"barriers"}, indent=1)
    user = (
        f"Condition: {ctx.case.condition}\n\n"
        f"## Patient case\n{case_view(ctx.case)}\n\n"
        f"## Case summary\nClinical: {summary.payload.clinical_summary}\n"
        f"Social: {summary.payload.social_summary}\n\n"
        f"## Flagged barriers\n{flagged}"
    )
    task_conditions = {t["id"]: t["conditions"] for t in ctx.taxonomy["tasks"]}

    def accept(d: TaskDetection):
        errors = check_against_taxonomy(ctx.taxonomy, ctx.case.condition, barriers.payload, d)
        warnings = []
        for t in d.tasks:
            if t.task_id in task_conditions and ctx.case.condition not in task_conditions[t.task_id]:
                errors.append(f"{t.task_id} does not apply to condition {ctx.case.condition}")
            e, w = check_evidence(ctx.case, t.evidence, t.task_id)
            errors += e
            warnings += w
        if errors:
            raise Rejected(errors)
        return d, warnings

    if not barriers.payload.barriers:
        return make_message(ctx, STAGE, TaskDetection(), [summary, barriers], ["no barriers flagged; no tasks"])
    payload, warnings = call_llm(ctx, STAGE, system_prompt(ctx.taxonomy), user, TaskDetection, accept)
    return make_message(ctx, STAGE, payload, [summary, barriers], warnings, llm=True)
