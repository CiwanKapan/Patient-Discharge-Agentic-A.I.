"""Gold-standard answer key and targeted test scenario models."""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from src.models.case import PatientCase
from src.models.messages import BarrierId, TaskId


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class KeyBarrier(_Strict):
    barrier_id: str = BarrierId
    evidence_fields: list[str] = Field(min_length=1)
    cross_field: bool


class KeyTask(_Strict):
    task_id: str = TaskId
    resolves: list[str] = Field(min_length=1)


class KeyInformationGap(_Strict):
    field: str
    candidate_barrier_id: str = BarrierId


class AnswerKey(_Strict):
    case_id: str
    barriers: list[KeyBarrier] = Field(default_factory=list)
    tasks: list[KeyTask] = Field(default_factory=list)
    information_gaps: list[KeyInformationGap] = Field(
        default_factory=list,
        description="Undocumented items a careful system should ask about, not flag as barriers.",
    )
    must_not_flag: list[str] = Field(
        default_factory=list,
        description="Negative controls: barrier IDs that look plausible but are wrong for this case.",
    )
    notes: Optional[str] = None


class Scenario(_Strict):
    """A small, hand-built case + key that isolates one reasoning skill."""

    scenario_id: str
    purpose: str
    case: PatientCase
    answer_key: AnswerKey
