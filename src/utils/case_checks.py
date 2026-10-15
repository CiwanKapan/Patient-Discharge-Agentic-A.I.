"""Deterministic case readings shared by the Case Analyzer, tests, and evaluation.

These helpers never decide on their own that a barrier exists. They produce the
single-field readings and time windows that the LLM stages reason over, and a
reference check used to verify that the cross-field scenario answer keys are
internally consistent.
"""
from __future__ import annotations

from typing import Literal

from src.models.case import (
    TRACKED_FIELD_NAMES,
    FieldReading,
    FieldStatus,
    PatientCase,
    read_field,
)
from src.models.messages import FieldSnapshot, TimeConstraint


def snapshot_fields(case: PatientCase) -> list[FieldSnapshot]:
    """One reading per tracked field. Omitted fields appear as status 'unknown'."""
    out = []
    for name in TRACKED_FIELD_NAMES:
        f = case.field(name)
        out.append(
            FieldSnapshot(
                field=f"tracked_fields.{name}",
                status=f.status if f else FieldStatus.UNKNOWN,
                reading=read_field(f),
            )
        )
    return out


def time_constraints(case: PatientCase) -> list[TimeConstraint]:
    out = []
    if case.planned_discharge_window:
        out.append(TimeConstraint(field="planned_discharge_window", window=case.planned_discharge_window))
    for name in TRACKED_FIELD_NAMES:
        f = case.field(name)
        if f and f.window:
            out.append(TimeConstraint(field=f"tracked_fields.{name}", window=f.window, note=f.detail))
    return out


TimingResult = Literal["conflict", "compatible", "not_arranged", "not_needed", "unknown"]


def transport_timing(case: PatientCase) -> TimingResult:
    """Reference reading for B-S07 (transport timing conflict).

    conflict      transport is arranged, but its window does not overlap the discharge window
    compatible    both windows are known and they overlap
    not_arranged  transport is documented as not arranged (that is B-S02, not B-S07)
    not_needed    transport is documented as not applicable
    unknown       transport status, its window, or the discharge window is not documented
    """
    transport = case.field("transport_status")
    reading = read_field(transport)
    if reading is FieldReading.INCOMPLETE:
        return "not_arranged"
    if reading is FieldReading.MISSING:
        return "unknown"
    if transport.status is FieldStatus.NOT_APPLICABLE:
        return "not_needed"
    if transport.window is None or case.planned_discharge_window is None:
        return "unknown"
    return "compatible" if transport.window.overlaps(case.planned_discharge_window) else "conflict"
