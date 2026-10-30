"""Stage 02 - Case Analyzer (LLM + deterministic readings).

Field readings and time windows are computed in code (src/utils/case_checks.py)
so the model cannot misread a status. The model writes the clinical and social
summaries and points at the note passages later stages should look at.
"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from src.models.messages import AgentMessage, CaseSummary, EvidenceRef, Stage
from src.pipeline._common import (
    SUMMARY_OUTPUT_RULES,
    Rejected,
    RunContext,
    call_llm,
    case_view,
    check_evidence,
    make_message,
    snapshot_lines,
)
from src.utils.case_checks import snapshot_fields, time_constraints

STAGE = Stage.CASE_ANALYZER

SYSTEM = f"""You are the case analyzer in a supervised hospital discharge-coordination pipeline. \
You read one synthetic patient chart and write a structured summary that later stages use to find \
discharge barriers and pending tasks.

Write:
{SUMMARY_OUTPUT_RULES}
- notes_of_interest: passages in the free-text notes that matter for discharge readiness, such as a \
medication change, a contradiction with a tracked field, or a timing constraint. Use the field path \
(for example free_text_notes.case_manager_note) and copy the passage verbatim into quote.

Rules:
- Describe only what the chart documents. Do not decide which barriers exist; a later stage does that.
- A field that is unknown or absent is undocumented, not "not done". Say "not documented" for it.
- Some notes contain details that sound concerning but are documented as resolved or irrelevant. \
Report them as resolved; do not list them in notes_of_interest."""


class CaseNarrative(BaseModel):
    model_config = ConfigDict(extra="forbid")

    clinical_summary: str
    social_summary: str
    notes_of_interest: list[EvidenceRef] = Field(default_factory=list)


def run(ctx: RunContext, upstream: AgentMessage) -> AgentMessage[CaseSummary]:
    snapshots = snapshot_fields(ctx.case)
    windows = time_constraints(ctx.case)
    user = (
        f"## Patient case\n{case_view(ctx.case)}\n\n"
        f"## Field readings (computed from status)\n{snapshot_lines(snapshots)}"
    )

    def accept(n: CaseNarrative):
        errors, warnings = check_evidence(ctx.case, n.notes_of_interest, "notes_of_interest")
        if errors:
            raise Rejected(errors)
        summary = CaseSummary(
            clinical_summary=n.clinical_summary,
            social_summary=n.social_summary,
            field_snapshots=snapshots,
            time_constraints=windows,
            notes_of_interest=n.notes_of_interest,
        )
        return summary, warnings

    payload, warnings = call_llm(ctx, STAGE, SYSTEM, user, CaseNarrative, accept)
    return make_message(ctx, STAGE, payload, [upstream], warnings, llm=True)
