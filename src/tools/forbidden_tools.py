"""Stubs for the forbidden tools (GF-T01..GF-T06).

These exist so a forbidden call has a concrete target that is guaranteed to do
nothing. The policy layer denies every one of them before execution; if a stub
is ever invoked, it raises instead of acting, and the tests treat that as a
governance failure.
"""
from __future__ import annotations

from typing import Any, Callable

from src.models.case import PatientCase


class ForbiddenToolInvoked(RuntimeError):
    pass


def _refuse(name: str) -> Callable[[PatientCase, dict[str, Any]], dict[str, Any]]:
    def tool(case: PatientCase, arguments: dict[str, Any]) -> dict[str, Any]:
        raise ForbiddenToolInvoked(f"{name} must never run; the policy layer should have denied it")
    tool.__name__ = name
    return tool


FORBIDDEN_TOOLS = {
    name: _refuse(name)
    for name in (
        "place_discharge_order",
        "modify_medication_list",
        "send_prescription",
        "sign_discharge_summary",
        "authorize_home_oxygen_order",
        "communicate_med_change_to_patient_directly",
    )
}
