"""Contract tests for stages 05-08, tool calls, and the audit log."""
from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from src.models.audit import AuditLogLine, check_audit_trail
from src.models.messages import BarrierFinding, TaskFinding
from src.models.plan import (
    ApprovalClassification,
    ApprovalDecisions,
    ApprovalMessage,
    DischargePlan,
    DischargePlanMessage,
    PlannedAction,
    Recommendation,
    RecommendationSet,
)
from src.models.tools import PolicyDecision, PolicyLayerOutput, ToolCall, check_policy

T0 = datetime(2026, 3, 9, 8, 0, tzinfo=timezone.utc)

REBOOK = dict(
    recommendation_id="R1", rank=1, kind="complete_task", description="Rebook transport inside the discharge window",
    urgency="medium", owner_role="case_manager", task_id="T-CM04", barrier_ids=["B-S07"],
)
ESCALATE = dict(
    recommendation_id="R2", rank=2, kind="complete_task", description="Tell patient about furosemide dose change",
    urgency="high", owner_role="physician", task_id="T-MD07", barrier_ids=["B-E07"],
    proposed_action="communicate_medication_change_to_patient_or_caregiver",
)


def _approval(rid, cls, rule=None):
    return ApprovalClassification(
        recommendation_id=rid, classification=cls, requires_human_approval=cls == "requires_human_approval",
        matched_rule_id=rule, reason="test",
    )


# ---------------------------------------------------------------- policy layer
def test_forbidden_tool_cannot_be_allowed():
    with pytest.raises(ValidationError):
        PolicyDecision(call_id="c", tool_name="send_prescription", decision="allowed", rule_id="GF-T03", reason="x")
    with pytest.raises(ValidationError):
        PolicyDecision(call_id="c", tool_name="mystery_tool", decision="allowed", reason="x")


def test_results_only_for_allowed_calls():
    denied = PolicyDecision(call_id="c1", tool_name="send_prescription", decision="denied", rule_id="GF-T03", reason="x")
    with pytest.raises(ValidationError):
        PolicyLayerOutput(decisions=[denied], results=[{"call_id": "c1", "output": {}}])


def test_check_policy_against_taxonomy(taxonomy):
    good = PolicyLayerOutput(decisions=[
        PolicyDecision(call_id="a", tool_name="get_transport_status", decision="allowed", rule_id="GA-T07", reason="read only"),
        PolicyDecision(call_id="b", tool_name="place_discharge_order", decision="denied", rule_id="GF-T01", reason="forbidden"),
        PolicyDecision(call_id="c", tool_name="mystery_tool", decision="denied", reason="not on allowed list"),
    ])
    assert check_policy(taxonomy, good) == []
    bad = PolicyLayerOutput(decisions=[
        PolicyDecision(call_id="a", tool_name="get_transport_status", decision="denied", reason="oops"),
    ])
    assert check_policy(taxonomy, bad)


# ---------------------------------------------------------------- recommendations and approvals
def test_recommendation_kinds():
    Recommendation(recommendation_id="V1", rank=1, kind="verify_information", description="Confirm follow-up booked",
                   urgency="medium", owner_role="case_manager", information_gap_field="tracked_fields.followup_appointment_status")
    with pytest.raises(ValidationError):
        Recommendation(**{**REBOOK, "task_id": None})
    with pytest.raises(ValidationError):
        Recommendation(recommendation_id="V1", rank=1, kind="verify_information", description="x", urgency="low",
                       owner_role="nurse", information_gap_field="tracked_fields.pending_labs", barrier_ids=["B-C02"])


def _ranked(*ranks):
    return [{**REBOOK, "recommendation_id": f"R{i}", "rank": rank} for i, rank in enumerate(ranks)]


@pytest.mark.parametrize("ranks", [(1, 2, 3), (3, 1, 2), (1, 1, 2), (1, 1, 1), (1, 2, 2, 3)])
def test_valid_ranks_including_ties(ranks):
    RecommendationSet(recommendations=_ranked(*ranks))


@pytest.mark.parametrize("ranks", [(1, 2, 4), (2, 3, 4), (1, 1, 3), (2, 2)])
def test_ranks_must_start_at_1_and_skip_nothing(ranks):
    with pytest.raises(ValidationError):
        RecommendationSet(recommendations=_ranked(*ranks))


def test_approval_flag_must_match_classification():
    with pytest.raises(ValidationError):
        ApprovalClassification(recommendation_id="R2", classification="auto_safe", requires_human_approval=True, reason="x")
    with pytest.raises(ValidationError):
        ApprovalClassification(recommendation_id="R2", classification="requires_human_approval",
                               requires_human_approval=True, reason="missing rule")


def test_check_governance(taxonomy):
    from src.models.plan import check_governance

    recs = RecommendationSet(recommendations=[REBOOK, ESCALATE])
    ok = ApprovalDecisions(classifications=[_approval("R1", "auto_safe"), _approval("R2", "requires_human_approval", "GR-A04")])
    assert check_governance(taxonomy, recs, ok) == []

    # The classic governance failure: an approval-required action marked auto_safe.
    bad = ApprovalDecisions(classifications=[_approval("R1", "auto_safe"), _approval("R2", "auto_safe")])
    assert any("R2" in e for e in check_governance(taxonomy, recs, bad))

    missing = ApprovalDecisions(classifications=[_approval("R1", "auto_safe")])
    assert any("not classified" in e for e in check_governance(taxonomy, recs, missing))


def test_proposing_vs_calling_an_overlapping_name(taxonomy):
    """modify_medication_list is GR-A02 to propose but GF-T02 to call."""
    from src.models.plan import check_governance

    base = dict(recommendation_id="R1", rank=1, kind="complete_task", description="Reconcile medications",
                urgency="high", owner_role="pharmacist", task_id="T-PH01", barrier_ids=["B-C01"])
    proposed = RecommendationSet(recommendations=[{**base, "proposed_action": "modify_medication_list"}])
    assert check_governance(taxonomy, proposed, ApprovalDecisions(
        classifications=[_approval("R1", "requires_human_approval", "GR-A02")])) == []

    called = RecommendationSet(recommendations=[{**base, "proposed_tool_calls": [
        {"tool_name": "modify_medication_list", "requested_by": "05_rec_generator"}]}])
    assert check_governance(taxonomy, called, ApprovalDecisions(
        classifications=[_approval("R1", "requires_human_approval", "GR-A02")]))
    assert check_governance(taxonomy, called, ApprovalDecisions(
        classifications=[_approval("R1", "forbidden", "GF-T02")])) == []


def test_new_payloads_bind_to_their_stage():
    with pytest.raises(ValidationError):
        ApprovalMessage(run_id="r", case_id="c", stage="05_rec_generator", payload={})
    ApprovalMessage(run_id="r", case_id="c", stage="06_approval_gate", payload={})


# ---------------------------------------------------------------- audit trail
def _plan(denied):
    barrier = BarrierFinding(barrier_id="B-S07", urgency="medium", cross_field=True, rationale="x", evidence=[
        {"field": "tracked_fields.transport_status"}, {"field": "planned_discharge_window"}])
    task = TaskFinding(task_id="T-CM04", resolves=["B-S07"], owner_role="case_manager", urgency="medium",
                       evidence=[{"field": "tracked_fields.transport_status"}], rationale="x")
    rec = Recommendation(**REBOOK)
    return DischargePlan(case_id="SCN-XF-01", summary="Transport pickup is after the discharge window.",
                         barriers=[barrier], tasks=[task],
                         actions=[PlannedAction(recommendation=rec, approval=_approval("R1", "auto_safe"))],
                         denied_tool_calls=[denied])


def _trail():
    read = ToolCall(call_id="c1", tool_name="get_transport_status", requested_by="03_barrier_detector")
    bad = ToolCall(call_id="c2", tool_name="place_discharge_order", requested_by="05_rec_generator")
    denied = PolicyDecision(call_id="c2", tool_name="place_discharge_order", decision="denied", rule_id="GF-T01", reason="forbidden")
    raw = [
        {"event_type": "case_loaded", "details": {"source": "data/scenarios/SCN-XF-01.json", "case_sha256": "0" * 64, "schema_valid": True}},
        {"event_type": "tool_call", "details": {"call": read.model_dump(), "decision": "allowed", "output": {"window": "17:00-18:00"}}},
        {"event_type": "policy_decision", "details": {"call_id": "c1", "tool_name": "get_transport_status", "decision": "allowed", "rule_id": "GA-T07", "reason": "read only"}},
        {"event_type": "barrier_flagged", "details": {"barrier_id": "B-S07", "evidence_fields": ["tracked_fields.transport_status", "planned_discharge_window"], "urgency": "medium"}},
        {"event_type": "task_recommended", "details": {"task_id": "T-CM04", "owner_role": "case_manager", "linked_barrier_ids": ["B-S07"]}},
        {"event_type": "tool_call", "details": {"call": bad.model_dump(), "decision": "denied"}},
        {"event_type": "policy_decision", "details": denied.model_dump()},
        {"event_type": "approval_classification", "details": {"recommendation_id": "R1", "classification": "auto_safe", "requires_human_approval": False, "reason": "no approval rule"}},
        {"event_type": "output_emitted", "details": {"plan": _plan(denied).model_dump()}},
        {"event_type": "run_completed", "details": {"status": "succeeded", "model": "claude-haiku-5-5", "prompt_versions": {"03_barrier_detector": "v1"}, "tool_call_count": 2,
                                                    "started_at": T0.isoformat(), "completed_at": (T0 + timedelta(seconds=30)).isoformat()}},
    ]
    events = []
    for i, r in enumerate(raw):
        line = AuditLogLine.model_validate({"run_id": "run-1", "case_id": "SCN-XF-01", "sequence": i,
                                            "timestamp": (T0 + timedelta(seconds=i)).isoformat(), **r})
        # round-trip through JSONL exactly as the logger would write and read it
        events.append(AuditLogLine.model_validate_json(line.model_dump_json()).root)
    return events


def test_complete_trail_passes():
    events = _trail()
    assert [e.audit_id for e in events][0] == "AU-01" and events[-1].audit_id == "AU-08"
    assert check_audit_trail(events) == []


def _without(events, drop):
    kept = [e for e in events if not drop(e)]
    for i, e in enumerate(kept):
        e.sequence = i
    return kept


def _no_tool_calls(count):
    """A run whose log has no tool call events, reporting `count` calls in run_completed."""
    events = _without(_trail(), lambda e: e.event_type in ("tool_call", "policy_decision"))
    plan = next(e for e in events if e.event_type == "output_emitted").details.plan
    plan.denied_tool_calls = []
    events[-1].details.tool_call_count = count
    return events


def test_missing_event_type_fails():
    events = _without(_trail(), lambda e: e.event_type == "task_recommended")
    assert any("task_recommended" in err for err in check_audit_trail(events))


def test_tool_call_without_policy_decision_fails():
    events = _without(_trail(), lambda e: e.event_type == "policy_decision" and e.details.call_id == "c1")
    errors = check_audit_trail(events)
    assert any("policy decision" in err for err in errors)
    assert any("reports 2 tool calls but 1 policy_decision" in err for err in errors)


def test_run_with_zero_tool_calls_passes():
    assert check_audit_trail(_no_tool_calls(0)) == []


def test_dropped_tool_call_events_are_not_mistaken_for_no_calls():
    errors = check_audit_trail(_no_tool_calls(2))
    assert any("reports 2 tool calls but 0 tool_call events" in err for err in errors)
    assert any("missing tool_call event" in err for err in errors)


def test_dropped_pair_of_events_is_caught_by_count():
    """Dropping a call and its decision together keeps them paired, so only the count catches it."""
    events = _without(_trail(), lambda e: e.event_type in ("tool_call", "policy_decision")
                      and (getattr(e.details, "call_id", None) or e.details.call.call_id) == "c1")
    assert any("reports 2 tool calls but 1 tool_call events" in err for err in check_audit_trail(events))


def test_count_lower_than_logged_calls_fails():
    events = _trail()
    events[-1].details.tool_call_count = 1
    assert any("reports 1 tool calls but 2 tool_call events" in err for err in check_audit_trail(events))


def test_same_tool_call_logged_twice_fails():
    events = _trail()
    dup = events[1].model_copy(deep=True)
    events.insert(2, dup)
    for i, e in enumerate(events):
        e.sequence = i
        e.timestamp = T0 + timedelta(seconds=i)
    assert any("logged more than once" in err for err in check_audit_trail(events))


def test_audit_id_must_match_event_type():
    with pytest.raises(ValidationError):
        AuditLogLine.model_validate({"run_id": "r", "case_id": "c", "sequence": 0, "audit_id": "AU-05",
                                     "event_type": "case_loaded",
                                     "details": {"source": "x", "case_sha256": "0" * 64, "schema_valid": True}})


def test_plan_message_envelope():
    msg = DischargePlanMessage(run_id="r", case_id="SCN-XF-01", stage="08_output_composer",
                               payload=_plan(PolicyDecision(call_id="c2", tool_name="place_discharge_order",
                                                            decision="denied", rule_id="GF-T01", reason="x")))
    assert msg.payload.actions[0].approval.classification == "auto_safe"
