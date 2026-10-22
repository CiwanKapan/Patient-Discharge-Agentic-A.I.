"""Stage 03 - Barrier Detector (LLM).

Flags discharge barriers from the closed taxonomy and reports undocumented items
as information gaps. Output is rejected if it breaks the taxonomy (unknown IDs,
wrong condition, wrong cross_field flag), cites evidence the chart does not
contain, or flags a barrier whose only evidence is a field the chart leaves
undocumented (that is an information gap, not a barrier).
"""
from __future__ import annotations

from src.models.case import FieldReading
from src.models.messages import AgentMessage, BarrierDetection, CaseSummary, Stage, check_against_taxonomy
from src.pipeline._common import (
    CHART_READING_RULES,
    Rejected,
    RunContext,
    barrier_reference,
    call_llm,
    case_view,
    check_evidence,
    check_path,
    field_reading,
    make_message,
    snapshot_lines,
)

STAGE = Stage.BARRIER_DETECTOR


def system_prompt(taxonomy: dict) -> str:
    return f"""You are the barrier detector in a supervised hospital discharge-coordination pipeline. \
You decide which discharge barriers a synthetic patient case has, using only the closed taxonomy below.

## Barrier taxonomy
{barrier_reference(taxonomy)}

{CHART_READING_RULES}

## Output rules
- Use only barrier IDs whose conditions include the case's condition.
- Set cross_field exactly as the taxonomy says. A cross_field barrier must cite at least two \
distinct evidence fields.
- Every barrier cites evidence: the field path (tracked_fields.<name>, planned_discharge_window, or \
free_text_notes.<note>), the field's status when citing a tracked field, and a verbatim quote when \
citing a note.
- Never report the same barrier ID as both a barrier and an information gap.
- information_gaps[].field is the path of the undocumented field.
- Use the taxonomy urgency unless the chart clearly supports a different one."""


def run(ctx: RunContext, summary: AgentMessage[CaseSummary]) -> AgentMessage[BarrierDetection]:
    s = summary.payload
    windows = "\n".join(f"- {w.field}: {w.window.start.isoformat()} to {w.window.end.isoformat()}"
                        for w in s.time_constraints) or "- none documented"
    notes = "\n".join(f"- {n.field}: {n.quote or ''}" for n in s.notes_of_interest) or "- none"
    user = (
        f"Condition: {ctx.case.condition}\n\n"
        f"## Patient case\n{case_view(ctx.case)}\n\n"
        f"## Case summary\nClinical: {s.clinical_summary}\nSocial: {s.social_summary}\n\n"
        f"## Field readings\n{snapshot_lines(s.field_snapshots)}\n\n"
        f"## Time windows\n{windows}\n\n"
        f"## Notes of interest\n{notes}"
    )

    def accept(d: BarrierDetection):
        errors = check_against_taxonomy(ctx.taxonomy, ctx.case.condition, d)
        warnings = []
        for b in d.barriers:
            e, w = check_evidence(ctx.case, b.evidence, b.barrier_id)
            errors += e
            warnings += w
            if e:
                continue
            tracked = [r.field for r in b.evidence if r.field.startswith("tracked_fields.")]
            if (not b.cross_field and tracked and len(tracked) == len(b.evidence)
                    and all(field_reading(ctx.case, f) is FieldReading.MISSING for f in tracked)):
                errors.append(f"{b.barrier_id}: every cited field is undocumented; report it as an information gap")
        for g in d.information_gaps:
            # An undocumented discharge window is a valid gap even though the path holds nothing.
            problem = None if g.field == "planned_discharge_window" else check_path(ctx.case, g.field)
            if problem:
                errors.append(f"information gap {g.candidate_barrier_id}: {problem}")
            elif (g.field.startswith("tracked_fields.")
                  and field_reading(ctx.case, g.field) is FieldReading.INCOMPLETE):
                warnings.append(f"information gap {g.candidate_barrier_id}: {g.field} is documented as not done")
        if errors:
            raise Rejected(errors)
        return d, warnings

    payload, warnings = call_llm(ctx, STAGE, system_prompt(ctx.taxonomy), user, BarrierDetection, accept)
    return make_message(ctx, STAGE, payload, [summary], warnings, llm=True)
