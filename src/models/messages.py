"""Standard message contract between pipeline stages.

Every stage emits the same envelope (``AgentMessage``) and only the ``payload``
type changes. That gives each hand-off the same metadata (run, case, stage,
model, prompt version, upstream message ids) so a bad output can be traced back
to the exact message that produced it.

    02 Case Analyzer    -> AgentMessage[CaseSummary]
    03 Barrier Detector -> AgentMessage[BarrierDetection]   (reads CaseSummary)
    04 Task Detector    -> AgentMessage[TaskDetection]      (reads CaseSummary + BarrierDetection)
    05 Rec. Generator   -> AgentMessage[RecommendationSet]  (src/models/plan.py)
    06 Approval Gate    -> AgentMessage[ApprovalDecisions]  (src/models/plan.py)
    07 Policy Layer     -> AgentMessage[PolicyLayerOutput]  (src/models/tools.py)
    08 Output Composer  -> AgentMessage[DischargePlan]      (src/models/plan.py)

Each payload class declares the stage that produces it in a ``STAGE`` class
variable; the envelope rejects a payload sent under any other stage.

LLM stages must return JSON that validates against these models. A response
that fails validation is rejected and logged; it is never repaired silently.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import ClassVar, Generic, Literal, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field, model_validator

from src.models.case import FieldReading, FieldStatus, TimeWindow

SCHEMA_VERSION = "1.0"

BarrierId = Field(pattern=r"^B-[CEFS]\d{2}$")
TaskId = Field(pattern=r"^T-(MD|RN|PH|CM)\d{2}$")
Urgency = Literal["high", "medium", "low"]
OwnerRole = Literal[
    "case_manager", "nurse", "pharmacist", "physical_therapist", "physician", "social_worker"
]


class Stage(str, Enum):
    INPUT_READER = "01_input_reader"
    CASE_ANALYZER = "02_case_analyzer"
    BARRIER_DETECTOR = "03_barrier_detector"
    TASK_DETECTOR = "04_task_detector"
    REC_GENERATOR = "05_rec_generator"
    APPROVAL_GATE = "06_approval_gate"
    POLICY_LAYER = "07_policy_layer"
    OUTPUT_COMPOSER = "08_output_composer"
    SIGNOFF_REQUEST = "09_signoff_request"


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class EvidenceRef(_Strict):
    """A pointer into the case that supports a finding.

    ``field`` is a dotted path into PatientCase, e.g.
    ``tracked_fields.transport_status``, ``planned_discharge_window`` or
    ``free_text_notes.case_manager_note``.
    """

    field: str = Field(pattern=r"^(tracked_fields\.[a-z_]+|planned_discharge_window|free_text_notes\.[a-z_]+)$")
    status: Optional[FieldStatus] = None
    quote: Optional[str] = Field(None, description="Verbatim chart text or value relied on.")


# ------------------------------------------------------------------ 02 Case Analyzer
class FieldSnapshot(_Strict):
    """Single-field reading computed deterministically from the case."""

    field: str
    status: FieldStatus
    reading: FieldReading


class TimeConstraint(_Strict):
    """Any documented time window, surfaced so later stages can compare them."""

    field: str
    window: TimeWindow
    note: Optional[str] = None


class CaseSummary(_Strict):
    STAGE: ClassVar[Stage] = Stage.CASE_ANALYZER

    clinical_summary: str
    social_summary: str
    field_snapshots: list[FieldSnapshot]
    time_constraints: list[TimeConstraint] = Field(default_factory=list)
    notes_of_interest: list[EvidenceRef] = Field(default_factory=list)


# ------------------------------------------------------------------ 03 Barrier Detector
class BarrierFinding(_Strict):
    barrier_id: str = BarrierId
    urgency: Urgency
    cross_field: bool = Field(
        description="True when the barrier only exists because of how two or more "
        "facts relate (e.g. transport window vs discharge window)."
    )
    evidence: list[EvidenceRef] = Field(min_length=1)
    rationale: str

    @model_validator(mode="after")
    def _cross_field_needs_two_sources(self) -> "BarrierFinding":
        if self.cross_field and len({e.field for e in self.evidence}) < 2:
            raise ValueError("a cross-field barrier must cite at least two distinct evidence fields")
        return self


class InformationGap(_Strict):
    """Information needed to rule a barrier in or out is not documented.

    This is NOT a barrier. It is scored separately and turns into a
    verification action rather than a discharge-blocking finding.
    """

    field: str
    candidate_barrier_id: str = BarrierId
    question: str = Field(description="What a human should confirm, e.g. 'Is a follow-up booked?'")


class BarrierDetection(_Strict):
    STAGE: ClassVar[Stage] = Stage.BARRIER_DETECTOR

    barriers: list[BarrierFinding] = Field(default_factory=list)
    information_gaps: list[InformationGap] = Field(default_factory=list)

    @model_validator(mode="after")
    def _no_double_counting(self) -> "BarrierDetection":
        flagged = {b.barrier_id for b in self.barriers}
        both = flagged & {g.candidate_barrier_id for g in self.information_gaps}
        if both:
            raise ValueError(f"reported as both barrier and information gap: {sorted(both)}")
        return self


# ------------------------------------------------------------------ 04 Task Detector
class TaskFinding(_Strict):
    task_id: str = TaskId
    resolves: list[str] = Field(min_length=1, description="Barrier IDs this task resolves.")
    owner_role: OwnerRole
    urgency: Urgency
    evidence: list[EvidenceRef] = Field(min_length=1)
    rationale: str


class TaskDetection(_Strict):
    STAGE: ClassVar[Stage] = Stage.TASK_DETECTOR

    tasks: list[TaskFinding] = Field(default_factory=list)


# ------------------------------------------------------------------ envelope
P = TypeVar("P", bound=BaseModel)


class AgentMessage(_Strict, Generic[P]):
    schema_version: Literal["1.0"] = SCHEMA_VERSION
    message_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    run_id: str
    case_id: str
    stage: Stage
    produced_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    model: Optional[str] = Field(None, description="Model id for LLM stages, null for deterministic code.")
    prompt_version: Optional[str] = None
    upstream: list[str] = Field(default_factory=list, description="message_ids this message was built from.")
    payload: P
    warnings: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _stage_matches_payload(self) -> "AgentMessage":
        expected = getattr(type(self.payload), "STAGE", None)
        if expected is not None and expected is not self.stage:
            raise ValueError(f"{type(self.payload).__name__} must come from stage {expected.value}")
        return self


CaseSummaryMessage = AgentMessage[CaseSummary]
BarrierDetectionMessage = AgentMessage[BarrierDetection]
TaskDetectionMessage = AgentMessage[TaskDetection]


# ------------------------------------------------------------------ taxonomy checks
def check_against_taxonomy(
    taxonomy: dict,
    condition: str,
    barriers: BarrierDetection,
    tasks: Optional[TaskDetection] = None,
) -> list[str]:
    """Return contract violations that need the taxonomy to detect (empty list = OK).

    Checks that IDs exist, fit the case's condition, that the cross_field flag
    matches the taxonomy, and that each task resolves a barrier that was
    actually flagged and that the taxonomy says it can resolve.
    """
    b_tax = {b["id"]: b for b in taxonomy["barriers"]}
    t_tax = {t["id"]: t for t in taxonomy["tasks"]}
    errors: list[str] = []

    for b in barriers.barriers:
        ref = b_tax.get(b.barrier_id)
        if ref is None:
            errors.append(f"unknown barrier {b.barrier_id}")
            continue
        if condition not in ref["conditions"]:
            errors.append(f"{b.barrier_id} does not apply to condition {condition}")
        if b.cross_field != ref["cross_field"]:
            errors.append(f"{b.barrier_id} cross_field={b.cross_field}, taxonomy says {ref['cross_field']}")
    for g in barriers.information_gaps:
        if g.candidate_barrier_id not in b_tax:
            errors.append(f"unknown barrier {g.candidate_barrier_id} in information gap")

    if tasks is not None:
        flagged = {b.barrier_id for b in barriers.barriers}
        for t in tasks.tasks:
            ref = t_tax.get(t.task_id)
            if ref is None:
                errors.append(f"unknown task {t.task_id}")
                continue
            if t.owner_role not in ref["owner_roles"]:
                errors.append(f"{t.task_id} owner {t.owner_role} not in {ref['owner_roles']}")
            for bid in t.resolves:
                if bid not in ref["resolves"]:
                    errors.append(f"{t.task_id} cannot resolve {bid} per taxonomy")
                if bid not in flagged:
                    errors.append(f"{t.task_id} resolves {bid}, which was not flagged")
    return errors
