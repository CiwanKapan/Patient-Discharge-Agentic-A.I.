"""End-to-end and per-stage tests for the pipeline, run offline with stand-in LLMs."""
import json
from pathlib import Path

import pytest

from evaluation.metrics import score_case
from src.models.answer_key import AnswerKey, Scenario
from src.models.audit import check_audit_trail
from src.models.case import PatientCase
from src.models.messages import BarrierDetection, Stage, TaskDetection
from src.pipeline import run_case
from src.pipeline._common import case_view
from src.utils.audit_logger import AuditLogger, read_audit_log

from oracle_llm import OracleLLM, ScriptedLLM

ROOT = Path(__file__).resolve().parent.parent
CASES = sorted((ROOT / "data" / "synthetic_cases").glob("*.json"))
SCENARIOS = sorted((ROOT / "data" / "scenarios").glob("*.json"))


def _load(path):
    case = PatientCase.model_validate_json(path.read_text())
    key = AnswerKey.model_validate_json((ROOT / "data" / "answer_keys" / f"{case.case_id}.key.json").read_text())
    return case, key


def _assert_perfect(key, plan, taxonomy):
    s = score_case(key, BarrierDetection(barriers=plan.barriers, information_gaps=plan.information_gaps),
                   TaskDetection(tasks=plan.tasks), actions=plan.actions, taxonomy=taxonomy).summary()
    assert s["approval_precision"] == s["approval_recall"] == 1.0 and s["approval_label_omissions"] == 0
    assert s["barrier_precision"] == s["barrier_recall"] == s["task_precision"] == s["task_recall"] == 1.0
    assert s["information_gap_recall"] == 1.0
    assert s["gap_misflags"] == s["negative_control_hits"] == s["task_link_mismatches"] == 0


# ---------------------------------------------------------------- end to end
@pytest.mark.parametrize("path", CASES[::10], ids=lambda p: p.stem)
def test_oracle_run_is_perfect_and_fully_audited(path, taxonomy, tmp_path):
    case, key = _load(path)
    r = run_case(path, OracleLLM(case, key, taxonomy), taxonomy=taxonomy, audit_dir=tmp_path)
    assert r.status == "succeeded", r.error
    assert r.audit_errors == []
    _assert_perfect(key, r.plan, taxonomy)
    assert [m.stage for m in r.messages] == list(Stage)


@pytest.mark.parametrize("path", SCENARIOS, ids=lambda p: p.stem)
def test_oracle_run_on_scenarios(path, taxonomy, tmp_path):
    scn = Scenario.model_validate_json(path.read_text())
    case_file = tmp_path / f"{scn.case.case_id}.json"
    case_file.write_text(scn.case.model_dump_json())
    r = run_case(case_file, OracleLLM(scn.case, scn.answer_key, taxonomy), taxonomy=taxonomy, audit_dir=tmp_path)
    assert r.status == "succeeded", r.error
    assert r.audit_errors == []
    _assert_perfect(scn.answer_key, r.plan, taxonomy)


def test_messages_chain_upstream(taxonomy, tmp_path):
    case, key = _load(CASES[0])
    r = run_case(CASES[0], OracleLLM(case, key, taxonomy), taxonomy=taxonomy, audit_dir=tmp_path)
    ids = set()
    for m in r.messages:
        assert m.run_id == r.run_id and m.case_id == case.case_id
        assert set(m.upstream) <= ids
        assert (m.model is not None) == (m.prompt_version is not None)
        ids.add(m.message_id)
    by_stage = {m.stage: m for m in r.messages}
    assert by_stage[Stage.BARRIER_DETECTOR].model == "oracle"
    assert by_stage[Stage.APPROVAL_GATE].model is None


# ---------------------------------------------------------------- governance in the full run
def test_forbidden_and_unknown_tool_calls_are_denied_and_logged(taxonomy, tmp_path):
    path = next(p for p in CASES if _load(p)[1].tasks)
    case, key = _load(path)
    llm = OracleLLM(case, key, taxonomy, extra_tool_calls=["send_prescription", "mystery_tool", "get_transport_status"])
    r = run_case(path, llm, taxonomy=taxonomy, audit_dir=tmp_path)
    assert r.status == "succeeded", r.error
    assert r.audit_errors == []

    first = r.plan.actions[0]
    assert first.approval.classification == "forbidden"
    assert first.approval.matched_rule_id == "GF-T03"
    denied = {d.tool_name: d.rule_id for d in r.plan.denied_tool_calls}
    assert denied == {"send_prescription": "GF-T03", "mystery_tool": None}

    events = read_audit_log(r.audit_path)
    calls = [e.details for e in events if e.event_type == "tool_call"]
    assert {c.call.tool_name: c.decision for c in calls}["get_transport_status"] == "allowed"
    for c in calls:
        assert (c.output is not None) == (c.decision == "allowed")
    assert events[-1].details.tool_call_count == len(calls)


def test_approval_required_action_is_flagged(taxonomy, tmp_path):
    path = next(p for p in CASES if any(t.task_id == "T-MD07" for t in _load(p)[1].tasks))
    case, key = _load(path)
    r = run_case(path, OracleLLM(case, key, taxonomy), taxonomy=taxonomy, audit_dir=tmp_path)
    action = next(a for a in r.plan.actions if a.recommendation.task_id == "T-MD07")
    assert action.approval.requires_human_approval
    assert action.approval.matched_rule_id == "GR-A04"


# ---------------------------------------------------------------- rejection, retry, failure
def _first_with(pred):
    return next(p for p in CASES if pred(*_load(p)))


def test_barrier_on_undocumented_field_is_rejected_then_retried(taxonomy, tmp_path):
    path = _first_with(lambda c, k: k.barriers and any(g.field.startswith("tracked_fields.") for g in k.information_gaps))
    case, key = _load(path)
    oracle = OracleLLM(case, key, taxonomy)
    gap = next(g for g in key.information_gaps if g.field.startswith("tracked_fields."))
    bad = oracle._barrier_detector()
    bad["information_gaps"] = [g for g in bad["information_gaps"] if g["field"] != gap.field]
    bad["barriers"].append({
        "barrier_id": gap.candidate_barrier_id, "urgency": "high", "cross_field": False,
        "evidence": [{"field": gap.field, "status": "unknown"}], "rationale": "misread missing as not done",
    })
    llm = ScriptedLLM(oracle, {Stage.BARRIER_DETECTOR: [bad]})
    r = run_case(path, llm, taxonomy=taxonomy, audit_dir=tmp_path)
    assert r.status == "succeeded", r.error
    warnings = next(m for m in r.messages if m.stage is Stage.BARRIER_DETECTOR).warnings
    assert any("attempt 1 rejected" in w and "information gap" in w for w in warnings)
    _assert_perfect(key, r.plan, taxonomy)


@pytest.mark.parametrize("mutate, message", [
    (lambda d: d["barriers"][0].update(barrier_id="B-Z99"), "barrier_id"),
    (lambda d: d["barriers"][0]["evidence"][0].update(status="not_started" if d["barriers"][0]["evidence"][0].get("status") != "not_started" else "complete"), "chart says"),
    (lambda d: d["barriers"][0].update(evidence=[{"field": "tracked_fields.not_a_field"}]), "not a tracked field"),
])
def test_invalid_barrier_output_fails_the_run(taxonomy, tmp_path, mutate, message):
    path = _first_with(lambda c, k: any(b.evidence_fields[0].startswith("tracked_fields.") and not b.cross_field for b in k.barriers))
    case, key = _load(path)
    oracle = OracleLLM(case, key, taxonomy)
    oracle.key = key.model_copy(update={"barriers": sorted(key.barriers, key=lambda b: b.cross_field)})
    bad = oracle._barrier_detector()
    mutate(bad)
    llm = ScriptedLLM(oracle, {Stage.BARRIER_DETECTOR: [bad, bad]})
    r = run_case(path, llm, taxonomy=taxonomy, audit_dir=tmp_path)
    assert r.status == "failed"
    assert "03_barrier_detector" in r.error and message in r.error
    events = read_audit_log(r.audit_path)
    assert events[0].event_type == "case_loaded"
    assert events[-1].event_type == "run_completed"
    assert events[-1].details.status == "failed"
    assert not any(e.event_type == "output_emitted" for e in events)


def test_unknown_proposed_action_is_rejected(taxonomy, tmp_path):
    path = _first_with(lambda c, k: k.tasks)
    case, key = _load(path)
    oracle = OracleLLM(case, key, taxonomy)
    bad = oracle._rec_generator()
    bad["recommendations"][0]["proposed_action"] = "discharge_patient_now"
    r = run_case(path, ScriptedLLM(oracle, {Stage.REC_GENERATOR: [bad, bad]}), taxonomy=taxonomy, audit_dir=tmp_path)
    assert r.status == "failed"
    assert "discharge_patient_now" in r.error


def test_recommendations_must_cover_every_task_and_gap(taxonomy, tmp_path):
    path = _first_with(lambda c, k: len(k.tasks) >= 2)
    case, key = _load(path)
    oracle = OracleLLM(case, key, taxonomy)
    bad = oracle._rec_generator()
    bad["recommendations"] = bad["recommendations"][1:]
    for i, rec in enumerate(bad["recommendations"], 1):
        rec["recommendation_id"] = f"R{i}"
    r = run_case(path, ScriptedLLM(oracle, {Stage.REC_GENERATOR: [bad, bad]}), taxonomy=taxonomy, audit_dir=tmp_path)
    assert r.status == "failed"
    assert "has no recommendation" in r.error


def test_unparseable_output_is_rejected(taxonomy, tmp_path):
    case, key = _load(CASES[0])
    oracle = OracleLLM(case, key, taxonomy)
    r = run_case(CASES[0], ScriptedLLM(oracle, {Stage.CASE_ANALYZER: ["not json", "{}"]}), taxonomy=taxonomy,
                 audit_dir=tmp_path, max_attempts=2)
    assert r.status == "failed"
    assert r.error.count("rejected") == 2


# ---------------------------------------------------------------- input reader
def test_malformed_case_fails_loudly_and_is_logged(taxonomy, tmp_path):
    data = json.loads(CASES[0].read_text())
    data["condition"] = "XX"
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps(data))
    r = run_case(bad, OracleLLM(*_load(CASES[0]), taxonomy), taxonomy=taxonomy, audit_dir=tmp_path)
    assert r.status == "failed"
    assert r.case_id == data["case_id"]
    assert "condition" in r.error
    events = read_audit_log(r.audit_path)
    assert [e.event_type for e in events] == ["case_loaded", "run_completed"]
    assert events[0].details.schema_valid is False


def test_model_never_sees_dataset_metadata():
    case = _load(CASES[0])[0].model_copy(update={"distractors": ["D-01"], "policy_context": {"note": "kept"}})
    view = json.loads(case_view(case))
    assert view["policy_context"] == {"note": "kept"}
    assert "difficulty" not in view and "distractors" not in view
    assert view["case_id"] == case.case_id


# ---------------------------------------------------------------- audit logger
def test_audit_logger_never_overwrites(tmp_path):
    path = tmp_path / "run.jsonl"
    AuditLogger(path, "r", "c").close()
    with pytest.raises(FileExistsError):
        AuditLogger(path, "r", "c")


def test_audit_log_round_trips(taxonomy, tmp_path):
    case, key = _load(CASES[5])
    r = run_case(CASES[5], OracleLLM(case, key, taxonomy), taxonomy=taxonomy, audit_dir=tmp_path)
    events = read_audit_log(r.audit_path)
    assert check_audit_trail(events) == []
    assert [e.sequence for e in events] == list(range(len(events)))
    plan = next(e for e in events if e.event_type == "output_emitted").details.plan
    assert plan == r.plan
