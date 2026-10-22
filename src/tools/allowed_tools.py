"""Mock implementations of the allowed tools (GA-T01..GA-T11).

Every tool reads from the case chart only. Nothing touches a real EHR, and the
two tools with a side effect only produce an internal log entry or a draft for
human review. Tools run only after the policy layer allows the call.
"""
from __future__ import annotations

from typing import Any, Callable

from src.models.case import PatientCase

Tool = Callable[[PatientCase, dict[str, Any]], dict[str, Any]]


def _fields(case: PatientCase, *names: str) -> dict[str, Any]:
    out = {}
    for name in names:
        f = case.field(name)
        out[name] = f.model_dump(mode="json", exclude_none=True) if f else {"status": "unknown"}
    return out


def _reader(*names: str) -> Tool:
    def tool(case: PatientCase, arguments: dict[str, Any]) -> dict[str, Any]:
        return _fields(case, *names)
    return tool


def get_transport_status(case: PatientCase, arguments: dict[str, Any]) -> dict[str, Any]:
    out = _fields(case, "transport_status")
    w = case.planned_discharge_window
    out["planned_discharge_window"] = w.model_dump(mode="json") if w else None
    return out


def flag_for_review(case: PatientCase, arguments: dict[str, Any]) -> dict[str, Any]:
    return {"flagged": True, "case_id": case.case_id, "reason": arguments.get("reason", ""), "effect": "internal_log_only"}


def draft_patient_education(case: PatientCase, arguments: dict[str, Any]) -> dict[str, Any]:
    topic = arguments.get("topic") or arguments.get("reason", "")
    return {
        "status": "draft_for_review",
        "case_id": case.case_id,
        "topic": topic,
        "draft": f"[DRAFT - requires clinician review before use] Patient education: {topic}",
    }


ALLOWED_TOOLS: dict[str, Tool] = {
    "get_medication_list": _reader(
        "medication_reconciliation_status", "medication_availability_status", "medication_education_status"
    ),
    "get_pending_labs": _reader("pending_labs"),
    "get_pending_imaging": _reader("pending_imaging"),
    "get_pending_consults": _reader("pending_consult"),
    "get_followup_status": _reader("followup_appointment_status", "pcp_notification_status", "outpatient_therapy_status"),
    "get_equipment_status": _reader(
        "oxygen_requirement", "medical_device_education_status", "mobile_device_education_status", "home_health_referral_status"
    ),
    "get_transport_status": get_transport_status,
    "get_caregiver_info": _reader("caregiver_status"),
    "get_home_safety_status": _reader("home_safety_status"),
    "flag_for_review": flag_for_review,
    "draft_patient_education": draft_patient_education,
}
