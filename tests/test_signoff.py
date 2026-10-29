"""Stage 09: the sign-off request, logged as AU-09 (signoff_requested) when the plan is emitted."""
import json
from pathlib import Path

import pytest

from evaluation.evaluate import governance_errors
from src.models.answer_key import AnswerKey
from src.models.audit import check_audit_trail
from src.models.case import PatientCase
from src.models.messages import Stage
from src.models.plan import check_plan_status, gated_actions
from src.pipeline import run_case
from src.utils.audit_logger import read_audit_log

from oracle_llm import OracleLLM

ROOT = Path(__file__).resolve().parent.parent
CASES = sorted((ROOT / "data" / "synthetic_cases").glob("*.json"))
GATED = json.loads((ROOT / "config" / "taxonomy.json").read_text())["governance"]["task_approvals"]


def _load(path):
    case = PatientCase.model_validate_json(path.read_text())
    key = AnswerKey.model_validate_json((ROOT / "data" / "answer_keys" / f"{case.case_id}.key.json").read_text())
    return case, key


def _run(path, taxonomy, tmp_path, **oracle_kw):
    case, key = _load(path)
    return run_case(path, OracleLLM(case, key, taxonomy, **oracle_kw), taxonomy=taxonomy, audit_dir=tmp_path)


GATED_CASE = next(p for p in CASES if sum(t.task_id in GATED for t in _load(p)[1].tasks) >= 2)
UNGATED_CASE = next(p for p in CASES if _load(p)[1].tasks and not any(t.task_id in GATED for t in _load(p)[1].tasks))


def test_plan_is_emitted_pending_with_a_request_for_every_gated_action(taxonomy, tmp_path):
    r = _run(GATED_CASE, taxonomy, tmp_path)
    assert r.status == "succeeded", r.error
    assert r.audit_errors == []
    assert r.plan.status == "pending_clinician_signoff"
    req = r.signoff_request
    assert req.status == "pending_clinician_signoff"
    gated = [a.recommendation.recommendation_id for a in gated_actions(r.plan)]
    assert len(gated) >= 2 and [a.recommendation_id for a in req.actions] == gated
    assert {a.matched_rule_id for a in req.actions} == {a.approval.matched_rule_id for a in gated_actions(r.plan)}
    assert r.messages[-1].stage is Stage.SIGNOFF_REQUEST


def test_request_is_logged_once_right_after_the_plan(taxonomy, tmp_path):
    r = _run(GATED_CASE, taxonomy, tmp_path)
    events = read_audit_log(r.audit_path)
    types = [e.event_type for e in events]
    assert types.count("signoff_requested") == 1
    assert types.index("signoff_requested") == types.index("output_emitted") + 1
    req = events[types.index("signoff_requested")]
    assert req.audit_id == "AU-09" and req.details.status == "pending_clinician_signoff"


def test_plan_with_nothing_gated_still_requests_signoff(taxonomy, tmp_path):
    r = _run(UNGATED_CASE, taxonomy, tmp_path)
    assert r.status == "succeeded" and r.audit_errors == []
    assert r.signoff_request.actions == [] and r.plan.status == "pending_clinician_signoff"
    assert "signoff_requested" in [e.event_type for e in read_audit_log(r.audit_path)]
    assert r.messages[-1].warnings == ["no action needs clinician approval; the plan still awaits sign-off"]


def test_forbidden_actions_are_never_offered_for_signoff(taxonomy, tmp_path):
    r = _run(GATED_CASE, taxonomy, tmp_path, extra_tool_calls=["send_prescription"])
    forbidden = {a.recommendation.recommendation_id for a in r.plan.actions if a.approval.classification == "forbidden"}
    assert forbidden and not forbidden & {a.recommendation_id for a in r.signoff_request.actions}
    assert r.audit_errors == []


def test_a_plan_marked_final_is_a_governance_failure(taxonomy, tmp_path):
    r = _run(GATED_CASE, taxonomy, tmp_path)
    final = r.plan.model_copy(update={"status": "final"})
    assert check_plan_status(r.plan) == []
    assert check_plan_status(final) == ["plan marked final; it must be emitted pending_clinician_signoff"]
    assert any("plan marked final" in e for e in governance_errors(taxonomy, final))


def _tamper(events, fn):
    events = fn(events)
    for i, e in enumerate(events):
        e.sequence = i
    return events


@pytest.mark.parametrize("tamper, message", [
    (lambda ev: [e for e in ev if e.event_type != "signoff_requested"], "missing signoff_requested"),
    (lambda ev: ev[:-1] + [next(e for e in ev if e.event_type == "signoff_requested")] + ev[-1:], "more than once"),
])
def test_audit_check_catches_missing_or_repeated_requests(taxonomy, tmp_path, tamper, message):
    r = _run(GATED_CASE, taxonomy, tmp_path)
    events = _tamper(read_audit_log(r.audit_path), tamper)
    assert any(message in e for e in check_audit_trail(events))


def test_audit_check_requires_the_request_right_after_the_plan(taxonomy, tmp_path):
    r = _run(GATED_CASE, taxonomy, tmp_path)
    events = read_audit_log(r.audit_path)
    s = next(i for i, e in enumerate(events) if e.event_type == "signoff_requested")
    events.insert(1, events.pop(s))
    assert any("right after output_emitted" in e for e in check_audit_trail(_tamper(events, lambda x: x)))


def test_audit_check_catches_a_final_status_or_wrong_actions(taxonomy, tmp_path):
    r = _run(GATED_CASE, taxonomy, tmp_path)
    events = read_audit_log(r.audit_path)
    req = next(e for e in events if e.event_type == "signoff_requested")
    req.details = req.details.model_copy(update={"status": "final"})
    assert any("must be pending_clinician_signoff" in e for e in check_audit_trail(events))
    req.details = req.details.model_copy(update={"status": "pending_clinician_signoff",
                                                 "actions": req.details.actions[1:]})
    assert any("!= gated plan actions" in e for e in check_audit_trail(events))
    out = next(e for e in events if e.event_type == "output_emitted")
    out.details.plan = out.details.plan.model_copy(update={"status": "final"})
    assert any("plan marked final" in e for e in check_audit_trail(events))
