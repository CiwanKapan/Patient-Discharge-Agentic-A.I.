"""Patient case model (the input contract for the pipeline).

Key design rule: *missing information* and an *incomplete discharge task* are
different things and must never be collapsed into one another.

Every tracked discharge item is a ``TrackedField`` with an explicit ``status``:

    complete        documented as done                      -> no barrier
    in_progress     documented as started but not finished  -> barrier (incomplete task)
    not_started     documented as not done                  -> barrier (incomplete task)
    not_applicable  documented as not needed for this case  -> no barrier
    unknown         the chart says nothing reliable         -> information gap

A field that is absent from the case is read as ``unknown``. An information gap is
reported separately from barriers (see ``src/models/messages.py``) and becomes a
"verify" action, not a discharge barrier. This keeps an undocumented follow-up
appointment from being scored the same as one that is documented as unscheduled.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, create_model, model_validator

ConditionCode = Literal["HF", "CO", "PN", "OR", "ST"]
Difficulty = Literal["easy", "medium", "hard"]


class FieldStatus(str, Enum):
    COMPLETE = "complete"
    IN_PROGRESS = "in_progress"
    NOT_STARTED = "not_started"
    NOT_APPLICABLE = "not_applicable"
    UNKNOWN = "unknown"


class FieldReading(str, Enum):
    """How a single field should be read before any cross-field reasoning."""

    SATISFIED = "satisfied"            # complete or not_applicable
    INCOMPLETE = "incomplete"          # documented as not done -> candidate barrier
    MISSING = "missing"                # unknown or absent -> information gap
    # Note: a field can read SATISFIED on its own and still be part of a
    # cross-field barrier (e.g. transport arranged but at the wrong time).


INCOMPLETE_STATUSES = frozenset({FieldStatus.IN_PROGRESS, FieldStatus.NOT_STARTED})
SATISFIED_STATUSES = frozenset({FieldStatus.COMPLETE, FieldStatus.NOT_APPLICABLE})


class TimeWindow(BaseModel):
    """A closed time interval, e.g. a discharge window or a pickup window."""

    model_config = ConfigDict(extra="forbid")

    start: datetime
    end: datetime

    @model_validator(mode="after")
    def _ordered(self) -> "TimeWindow":
        if self.end <= self.start:
            raise ValueError("window end must be after start")
        return self

    def overlaps(self, other: "TimeWindow") -> bool:
        return self.start < other.end and other.start < self.end


class TrackedField(BaseModel):
    """One discharge item as documented in the chart."""

    model_config = ConfigDict(extra="forbid")

    status: FieldStatus
    detail: Optional[str] = Field(None, description="Chart text describing the item.")
    source: Optional[str] = Field(None, description="Where it was documented, e.g. 'nursing_flowsheet'.")
    documented_at: Optional[datetime] = None
    window: Optional[TimeWindow] = Field(
        None,
        description="Availability window for time-bound arrangements "
        "(transport pickup, caregiver availability). Needed for timing checks.",
    )
    scheduled_for: Optional[datetime] = Field(
        None, description="Date/time of a scheduled item, e.g. a follow-up appointment."
    )


# Every evidence field named in config/taxonomy.json, except free-text notes and
# planned_discharge_window, which live at the top level of PatientCase.
TRACKED_FIELD_NAMES = (
    "caregiver_status",
    "case_manager_status",
    "diet_education_status",
    "discharge_summary_status",
    "financial_status",
    "followup_appointment_status",
    "home_health_referral_status",
    "home_safety_status",
    "insurance_authorization_status",
    "medical_device_education_status",
    "medical_stability_status",
    "medication_availability_status",
    "medication_education_status",
    "medication_reconciliation_status",
    "mobile_device_education_status",
    "outpatient_therapy_status",
    "oxygen_requirement",
    "patient_education_status",
    "pcp_notification_status",
    "pending_consult",
    "pending_imaging",
    "pending_labs",
    "physical_function_status",
    "return_precautions_documented",
    "transport_status",
    "wound_status",
)

TrackedFields = create_model(
    "TrackedFields",
    __config__=ConfigDict(extra="forbid"),
    __doc__="All tracked discharge items. An omitted field is read as status 'unknown'.",
    **{n: (Optional[TrackedField], None) for n in TRACKED_FIELD_NAMES},
)


class FreeTextNotes(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_manager_note: Optional[str] = None
    nursing_note: Optional[str] = None
    physician_note: Optional[str] = None


class PatientCase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str
    condition: ConditionCode
    difficulty: Difficulty
    planned_discharge_window: Optional[TimeWindow] = Field(
        None, description="When discharge is planned. Absent means unknown."
    )
    tracked_fields: TrackedFields  # type: ignore[valid-type]
    free_text_notes: FreeTextNotes = Field(default_factory=FreeTextNotes)
    distractors: list[str] = Field(default_factory=list)
    policy_context: Optional[dict] = None

    def field(self, name: str) -> Optional[TrackedField]:
        if name not in TRACKED_FIELD_NAMES:
            raise KeyError(f"not a tracked field: {name}")
        return getattr(self.tracked_fields, name)


def read_field(field: Optional[TrackedField]) -> FieldReading:
    """Classify one field on its own. Absent fields are MISSING, never INCOMPLETE."""
    if field is None or field.status is FieldStatus.UNKNOWN:
        return FieldReading.MISSING
    if field.status in INCOMPLETE_STATUSES:
        return FieldReading.INCOMPLETE
    return FieldReading.SATISFIED
