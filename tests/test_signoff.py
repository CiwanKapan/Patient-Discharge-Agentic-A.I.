"""Stage 09: sign-off on gated actions, after the output composer."""
import json
from pathlib import Path

import pytest

from src.models.answer_key import AnswerKey
from src.models.audit import check_audit_trail
from src.models.case import PatientCase
from src.models.messages import Stage
from src.models.plan import gated_actions
from src.pipeline import run_case
from src.pipeline.runner import signoff
from src.utils.audit_logger import read_audit_log

from oracle_llm import OracleLLM

ROOT = Path(__file__).resolve().parent.parent
CASES = sorted((ROOT / "data" / "synthetic_cases").glob("*.json"))
GATED = json.loads((ROOT / "config" / "taxonomy.json").read_text())["governance"]["task_approvals"]


def _load(path):
    case = PatientCase.model_validate_json(path.read_text())
    key = AnswerKey.model_validate_json((ROOT / "data" / "answer_keys" / f"{case.case_id}.key.json").read_text())
    return case, key


def _run(path, taxonomy, tmp_path, reviewer=None, **oracle_kw):
    case, key = _load(path)
    return run_case(path, OracleLLM(case, key, taxonomy, **oracle_kw), taxonomy=taxonomy, audit_dir=tmp_path,
                    reviewer=reviewer)


GATED_CASE = next(p for p in CASES if sum(t.task_id in GATED for t in _load(p)[1].tasks) >= 2)
UNGATED_CASE = next(p for p in CASES if _load(p)[1].tasks and not any(t.task_id in GATED for t in _load(p)[1].tasks))


def test_default_leaves_every_gated_action_pending(taxonomy, tmp_path):
    r = _run(GATED_CASE, taxonomy, tmp_path)
    assert r.status == "succeeded", r.error
    assert r.audit_errors == []
    gated = [a.recommendation.recommendation_id for a in gated_actions(r.plan)]
    assert len(gated) >= 2
    assert [d.recommendation_id for d in r.signoffs] == gated
    assert all(d.decision == "pending" and d.reviewer == "none" for d in r.signoffs)
    assert r.messages[-1].stage is Stage.SIGNOFF


def test_signoff_is_logged_after_the_composed_plan(taxonomy, tmp_path):
    r = _run(GATED_CASE, taxonomy, tmp_path)
    events = read_audit_log(r.audit_path)
    types = [e.event_type for e in events]
    signed = [i for i, t in enumerate(types) if t == "signoff_recorded"]
    assert signed and min(signed) > types.index("output_emitted")
    assert types[-1] == "run_completed"
    assert {events[i].audit_id for i in signed} == {"AU-09"}
    plan = next(e for e in events if e.event_type == "output_emitted").details.plan
    assert plan == r.plan  # the logged plan is the composed one; sign-off does not edit it


def test_approve_all(taxonomy, tmp_path):
    r = _run(GATED_CASE, taxonomy, tmp_path, reviewer=signoff.ApproveAllReviewer())
    assert r.signoffs and all(d.decision == "approved" for d in r.signoffs)
    assert all(d.reviewer == "simulated:approve_all" for d in r.signoffs)
    assert {d.matched_rule_id for d in r.signoffs} == {a.approval.matched_rule_id for a in gated_actions(r.plan)}


def test_reviewer_can_reject_and_the_plan_is_unchanged(taxonomy, tmp_path):
    class RejectMedChanges:
        name = "test:reject_meds"

        def review(self, plan, action):
            if action.recommendation.task_id == "T-MD07":
                return "rejected", "Dose change not confirmed."
            return "approved", "ok"

    path = next(p for p in CASES if any(t.task_id == "T-MD07" for t in _load(p)[1].tasks))
    approved = _run(path, taxonomy, tmp_path / "a", reviewer=signoff.ApproveAllReviewer())
    r = _run(path, taxonomy, tmp_path / "b", reviewer=RejectMedChanges())
    assert r.audit_errors == []
    by_task = {d.task_id: d.decision for d in r.signoffs}
    assert by_task["T-MD07"] == "rejected"
    assert all(v == "approved" for t, v in by_task.items() if t != "T-MD07")
    assert r.plan.actions == approved.plan.actions


def test_forbidden_actions_are_never_offered_for_signoff(taxonomy, tmp_path):
    r = _run(GATED_CASE, taxonomy, tmp_path, reviewer=signoff.ApproveAllReviewer(),
             extra_tool_calls=["send_prescription"])
    forbidden = {a.recommendation.recommendation_id for a in r.plan.actions if a.approval.classification == "forbidden"}
    assert forbidden
    assert not forbidden & {d.recommendation_id for d in r.signoffs}
    assert r.audit_errors == []


def test_plan_with_nothing_gated_logs_no_signoff(taxonomy, tmp_path):
    r = _run(UNGATED_CASE, taxonomy, tmp_path)
    assert r.status == "succeeded" and r.signoffs == []
    assert r.audit_errors == []
    assert not any(e.event_type == "signoff_recorded" for e in read_audit_log(r.audit_path))
    assert r.messages[-1].warnings == ["no action needs sign-off"]


def test_invalid_reviewer_decision_fails_the_run(taxonomy, tmp_path):
    class Broken:
        name = "test:broken"

        def review(self, plan, action):
            return "maybe", "?"

    r = _run(GATED_CASE, taxonomy, tmp_path, reviewer=Broken())
    assert r.status == "failed" and "09_signoff" in r.error and r.plan is None
    assert any("signoff_recorded" in e for e in r.audit_errors)  # gated actions left without sign-off


@pytest.mark.parametrize("tamper, message", [
    (lambda ev: [e for e in ev if e.event_type != "signoff_recorded"], "!= gated plan actions"),
    (lambda ev: ev + [next(e for e in ev if e.event_type == "signoff_recorded")], "!= gated plan actions"),
])
def test_audit_check_catches_bad_signoff_trails(taxonomy, tmp_path, tamper, message):
    r = _run(GATED_CASE, taxonomy, tmp_path)
    events = tamper(read_audit_log(r.audit_path))
    assert any(message in e for e in check_audit_trail(events))


def test_audit_check_requires_signoff_after_the_plan(taxonomy, tmp_path):
    r = _run(GATED_CASE, taxonomy, tmp_path)
    events = read_audit_log(r.audit_path)
    s = next(i for i, e in enumerate(events) if e.event_type == "signoff_recorded")
    events.insert(1, events.pop(s))
    assert any("before output_emitted" in e for e in check_audit_trail(events))
