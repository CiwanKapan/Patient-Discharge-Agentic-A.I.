"""Checks on the targeted scenarios in data/scenarios/.

1. Every scenario parses and its answer key uses valid, condition-appropriate IDs.
2. Each answer key agrees with the deterministic field readings, so the key itself
   cannot quietly confuse "undocumented" with "not done".
3. Cross-field barriers really are cross-field: every field they cite reads as
   fine on its own, and the barrier only appears when the fields are compared.
4. The metrics reward a correct system and penalize the two failure modes the
   scenarios target.
"""
import json

import pytest

from evaluation.metrics import score_case
from scripts.export_schemas import ROOT
from src.models.answer_key import Scenario
from src.models.case import TRACKED_FIELD_NAMES, FieldReading, read_field
from src.models.messages import BarrierDetection
from src.utils.case_checks import transport_timing

FILES = sorted((ROOT / "data" / "scenarios").glob("*.json"))
SCENARIOS = {p.stem: Scenario.model_validate(json.loads(p.read_text())) for p in FILES}


def _field_name(path: str) -> str | None:
    return path.split(".", 1)[1] if path.startswith("tracked_fields.") else None


def test_scenarios_exist():
    assert any(s.answer_key.must_not_flag for s in SCENARIOS.values()), "need negative controls"
    assert any(b.cross_field for s in SCENARIOS.values() for b in s.answer_key.barriers)
    assert any(s.answer_key.information_gaps for s in SCENARIOS.values())


@pytest.mark.parametrize("sid", sorted(SCENARIOS))
def test_answer_key_uses_valid_ids(sid, taxonomy):
    s = SCENARIOS[sid]
    key = s.answer_key
    assert key.case_id == s.case.case_id == s.scenario_id
    b_tax = {b["id"]: b for b in taxonomy["barriers"]}
    t_tax = {t["id"]: t for t in taxonomy["tasks"]}
    for b in key.barriers:
        assert s.case.condition in b_tax[b.barrier_id]["conditions"]
        assert b.cross_field == b_tax[b.barrier_id]["cross_field"]
    flagged = {b.barrier_id for b in key.barriers}
    for t in key.tasks:
        assert set(t.resolves) <= set(t_tax[t.task_id]["resolves"]) & flagged
    for bid in key.must_not_flag + [g.candidate_barrier_id for g in key.information_gaps]:
        assert bid in b_tax
    assert not flagged & set(key.must_not_flag)


@pytest.mark.parametrize("sid", sorted(SCENARIOS))
def test_answer_key_matches_field_readings(sid, taxonomy):
    s = SCENARIOS[sid]
    case, key = s.case, s.answer_key
    readings = {n: read_field(case.field(n)) for n in TRACKED_FIELD_NAMES}
    single = {b["id"]: b["evidence_fields"] for b in taxonomy["barriers"] if not b["cross_field"]}

    # Every documented-as-not-done field is explained by a single-field barrier in the key.
    for name, r in readings.items():
        if r is FieldReading.INCOMPLETE:
            assert any(name in single.get(b.barrier_id, []) for b in key.barriers), f"{name} not keyed"

    # Every undocumented field is keyed as an information gap, never as a barrier.
    gap_fields = {_field_name(g.field) for g in key.information_gaps}
    for name, r in readings.items():
        if r is FieldReading.MISSING:
            assert name in gap_fields, f"{name} is undocumented but has no information gap"
    for g in key.information_gaps:
        name = _field_name(g.field)
        if g.candidate_barrier_id == "B-S07":
            assert transport_timing(case) == "unknown"
        else:
            assert readings[name] is FieldReading.MISSING


@pytest.mark.parametrize("sid", sorted(SCENARIOS))
def test_cross_field_barriers_are_invisible_field_by_field(sid):
    s = SCENARIOS[sid]
    for b in s.answer_key.barriers:
        if not b.cross_field:
            continue
        assert len(b.evidence_fields) >= 2
        for path in b.evidence_fields:
            name = _field_name(path)
            if name:
                assert read_field(s.case.field(name)) is FieldReading.SATISFIED, f"{path} already flags on its own"
        if b.barrier_id == "B-S07":
            assert transport_timing(s.case) == "conflict"
    if "B-S07" in s.answer_key.must_not_flag:
        assert transport_timing(s.case) != "conflict"


def _perfect(s):
    return BarrierDetection(
        barriers=[{"barrier_id": b.barrier_id, "urgency": "high", "cross_field": b.cross_field, "rationale": "-",
                   "evidence": [{"field": f} for f in b.evidence_fields]} for b in s.answer_key.barriers],
        information_gaps=[{"field": g.field, "candidate_barrier_id": g.candidate_barrier_id, "question": "?"}
                          for g in s.answer_key.information_gaps],
    )


def test_metrics_perfect_system():
    score = None
    for s in SCENARIOS.values():
        score = score_case(s.answer_key, _perfect(s), into=score)
    out = score.summary()
    assert out["barrier_recall"] == out["barrier_precision"] == out["cross_field_recall"] == 1.0
    assert out["information_gap_recall"] == 1.0
    assert out["gap_misflags"] == out["negative_control_hits"] == 0


def test_metrics_penalize_field_by_field_system():
    """A system that only looks at single-field statuses and treats unknown as not done."""
    score = None
    for s in SCENARIOS.values():
        flagged = []
        for name in TRACKED_FIELD_NAMES:
            if read_field(s.case.field(name)) is not FieldReading.SATISFIED:
                flagged.append({"barrier_id": {"followup_appointment_status": "B-F01", "pending_labs": "B-C02"}.get(name, "B-S02"),
                                "urgency": "high", "cross_field": False, "rationale": "-",
                                "evidence": [{"field": f"tracked_fields.{name}"}]})
        score = score_case(s.answer_key, BarrierDetection(barriers=flagged), into=score)
    out = score.summary()
    assert out["cross_field_recall"] == 0.0
    assert out["gap_misflags"] > 0
