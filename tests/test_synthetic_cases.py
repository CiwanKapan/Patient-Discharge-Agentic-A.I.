"""Checks on the stratified dataset in data/synthetic_cases/ and data/answer_keys/.

These are written independently of scripts/generate_cases.py so the generator
does not grade itself. They apply the same rules as tests/test_scenarios.py to
every case, plus the dataset-level design rules from the methodology:

* every case has a key; IDs exist and fit the condition
* incomplete fields are keyed as barriers; undocumented fields as information gaps
* cross-field barriers are invisible field by field
* difficulty rules (barrier counts, cross-field / note-hidden barriers, distractors)
* distractors are used per the distractor sheet's rules
* dataset targets (stratification, forbidden-tool temptations, cross-field share)
"""
import csv
import json
from collections import Counter

import pytest

from scripts.export_schemas import ROOT
from src.models.answer_key import AnswerKey
from src.models.case import TRACKED_FIELD_NAMES, FieldReading, PatientCase, read_field
from src.utils.case_checks import transport_timing

CASE_DIR = ROOT / "data" / "synthetic_cases"
KEY_DIR = ROOT / "data" / "answer_keys"
MANIFEST = ROOT / "data" / "dataset_manifest.csv"

CASES = {p.stem: PatientCase.model_validate(json.loads(p.read_text())) for p in sorted(CASE_DIR.glob("*.json"))}
KEYS = {p.name.removesuffix(".key.json"): AnswerKey.model_validate(json.loads(p.read_text()))
        for p in sorted(KEY_DIR.glob("*.key.json"))}
ROWS = {r["case_id"]: r for r in csv.DictReader(MANIFEST.open())} if MANIFEST.exists() else {}
IDS = sorted(CASES)

pytestmark = pytest.mark.skipif(not CASES, reason="no synthetic cases generated yet")


def _name(path):
    return path.split(".", 1)[1] if path.startswith("tracked_fields.") else None


def _all_notes(case):
    n = case.free_text_notes
    return " ".join(x for x in (n.case_manager_note, n.nursing_note, n.physician_note) if x)


def test_every_case_has_a_key_and_manifest_row():
    assert set(CASES) == set(KEYS)
    assert set(CASES) == set(ROWS)


@pytest.mark.parametrize("cid", IDS)
def test_key_ids_valid_for_condition(cid, taxonomy):
    case, key = CASES[cid], KEYS[cid]
    b_tax = {b["id"]: b for b in taxonomy["barriers"]}
    t_tax = {t["id"]: t for t in taxonomy["tasks"]}
    assert key.case_id == case.case_id == cid
    flagged = [b.barrier_id for b in key.barriers]
    assert len(flagged) == len(set(flagged))
    for b in key.barriers:
        assert case.condition in b_tax[b.barrier_id]["conditions"]
        assert b.cross_field == b_tax[b.barrier_id]["cross_field"]
    for t in key.tasks:
        assert set(t.resolves) <= set(t_tax[t.task_id]["resolves"]) & set(flagged)
    for bid in key.must_not_flag + [g.candidate_barrier_id for g in key.information_gaps]:
        assert bid in b_tax
    assert not set(flagged) & set(key.must_not_flag)


@pytest.mark.parametrize("cid", IDS)
def test_key_matches_field_readings(cid, taxonomy):
    case, key = CASES[cid], KEYS[cid]
    readings = {n: read_field(case.field(n)) for n in TRACKED_FIELD_NAMES}
    single = {b["id"]: b["evidence_fields"] for b in taxonomy["barriers"] if not b["cross_field"]}
    for name, r in readings.items():
        if r is FieldReading.INCOMPLETE:
            assert any(name in single.get(b.barrier_id, []) for b in key.barriers), f"{name} not keyed"
    gap_fields = {_name(g.field) for g in key.information_gaps}
    for name, r in readings.items():
        if r is FieldReading.MISSING:
            assert name in gap_fields, f"{name} undocumented but no information gap"
    for g in key.information_gaps:
        if g.candidate_barrier_id == "B-S07":
            assert transport_timing(case) == "unknown"
        else:
            assert readings[_name(g.field)] is FieldReading.MISSING
        assert g.candidate_barrier_id in key.must_not_flag


@pytest.mark.parametrize("cid", IDS)
def test_cross_field_and_note_evidence(cid):
    case, key = CASES[cid], KEYS[cid]
    notes = {k: v for k, v in case.free_text_notes.model_dump().items() if v}
    for b in key.barriers:
        for path in b.evidence_fields:
            if path.startswith("free_text_notes."):
                assert path.split(".", 1)[1] in notes, f"{b.barrier_id} cites an empty note"
        if b.cross_field:
            assert len(b.evidence_fields) >= 2
            for path in b.evidence_fields:
                if _name(path):
                    assert read_field(case.field(_name(path))) is FieldReading.SATISFIED
        if b.barrier_id == "B-S07":
            assert transport_timing(case) == "conflict"
    if "B-S07" in key.must_not_flag:
        assert transport_timing(case) != "conflict"


@pytest.mark.parametrize("cid", IDS)
def test_difficulty_rules(cid):
    case, key, row = CASES[cid], KEYS[cid], ROWS[cid]
    n = len(key.barriers)
    cross = any(b.cross_field for b in key.barriers)
    note_hidden = any(any(p.startswith("free_text_notes.") for p in b.evidence_fields) for b in key.barriers)
    n_dis = len(row["distractors"].split())
    if case.difficulty == "easy":
        assert 1 <= n <= 2 and not cross and not note_hidden and not key.information_gaps and n_dis == 0
        assert all(len(b.evidence_fields) == 1 for b in key.barriers)
    elif case.difficulty == "medium":
        assert 2 <= n <= 4 and n_dis == 1
        assert cross or note_hidden, "medium case needs a cross-field or note-surfaced barrier"
    else:
        assert n >= 4 and cross and note_hidden and 1 <= n_dis <= 2


@pytest.mark.parametrize("cid", IDS)
def test_distractor_rules(cid, distractors):
    case, key, row = CASES[cid], KEYS[cid], ROWS[cid]
    phrases = {p["id"]: p for p in distractors["phrases"]}
    used = row["distractors"].split()
    gold = {b.barrier_id for b in key.barriers}
    text = _all_notes(case)
    assert len({phrases[d]["group"] for d in used}) == len(used), "two distractors from one group"
    for d in used:
        p = phrases[d]
        assert case.condition in p["suitable_conditions"]
        assert not set(p["avoid_if_barriers"]) & gold, f"{d} overlaps a keyed barrier"
        assert p["text"] in text, f"{d} text not in the notes"
    assert not case.distractors, "distractor phrases belong in the notes, not a labelled list"


def test_dataset_targets():
    n = len(CASES)
    by_diff = Counter(c.difficulty for c in CASES.values())
    assert abs(by_diff["easy"] / n - 0.30) <= 0.02
    assert abs(by_diff["medium"] / n - 0.50) <= 0.02
    assert abs(by_diff["hard"] / n - 0.20) <= 0.02
    by_cond = Counter(c.condition for c in CASES.values())
    assert max(by_cond.values()) - min(by_cond.values()) <= 1
    tempt = sum(1 for r in ROWS.values() if r["forbidden_temptation"])
    assert abs(tempt / n - 0.20) <= 0.03
    cross = sum(1 for k in KEYS.values() if any(b.cross_field for b in k.barriers))
    assert cross / n >= 0.30
    used = Counter(b.barrier_id for k in KEYS.values() for b in k.barriers)
    assert len(used) == 26, "every barrier in the taxonomy appears at least once"
    assert sum("B-S07" in k.must_not_flag for k in KEYS.values()) >= 10, "need B-S07 negative controls"


@pytest.mark.parametrize("cid", [c for c in IDS if ROWS.get(c, {}).get("forbidden_temptation")])
def test_temptation_is_in_the_notes(cid, taxonomy):
    tool = ROWS[cid]["forbidden_temptation"]
    assert tool in {t["id"] for t in taxonomy["governance"]["forbidden_tools"]}
    assert CASES[cid].free_text_notes.case_manager_note


def test_b_e02_task_follows_the_charted_reason():
    """Medication not available: prior authorization -> T-PH03, anything else -> T-PH02 (eval and dev keys)."""
    from src.utils.run_records import CASE_SETS, case_files
    checked = 0
    for case_dir, key_dir, _ in CASE_SETS.values():
        for p in case_files(case_dir):
            case = json.loads(p.read_text())
            key = json.loads((key_dir / f"{p.stem}.key.json").read_text())
            b = next((x for x in key["barriers"] if x["barrier_id"] == "B-E02"), None)
            if b is None:
                continue
            text = " ".join(json.dumps(case["tracked_fields"].get(f.split(".", 1)[1], "")) if f.startswith("tracked_fields.")
                            else case["free_text_notes"].get(f.split(".", 1)[1], "") for f in b["evidence_fields"])
            expected = "T-PH03" if "prior authorization" in text.lower() else "T-PH02"
            assert [t["task_id"] for t in key["tasks"] if "B-E02" in t["resolves"]] == [expected], p.stem
            checked += 1
    assert checked >= 17


def test_b_f02_keys_follow_the_taxonomy_windows_where_set(taxonomy):
    """Where taxonomy 2.2 sets a safe follow-up window, B-F02 is keyed exactly when the follow-up is
    more whole calendar days after the planned discharge date than the window allows."""
    from datetime import date
    from src.utils.run_records import CASE_SETS, case_files
    windows = next(b for b in taxonomy["barriers"] if b["id"] == "B-F02")["safe_followup_window_days"]
    checked = 0
    for case_dir, key_dir, _ in CASE_SETS.values():
        for p in case_files(case_dir):
            case = json.loads(p.read_text())
            days = (windows.get(case["condition"]) or {}).get("days")
            fu = case["tracked_fields"].get("followup_appointment_status") or {}
            if days is None or not fu.get("scheduled_for") or not case.get("planned_discharge_window"):
                continue
            gap = (date.fromisoformat(fu["scheduled_for"][:10]) - date.fromisoformat(case["planned_discharge_window"]["start"][:10])).days
            key = json.loads((key_dir / f"{p.stem}.key.json").read_text())
            assert any(b["barrier_id"] == "B-F02" for b in key["barriers"]) == (gap > days), (p.stem, gap)
            checked += 1
    assert checked > 0


def test_b_f02_windows_reach_the_prompt_only_when_complete(taxonomy):
    import copy
    from src.pipeline._common import barrier_reference
    assert "Safe follow-up window" not in barrier_reference(taxonomy)  # values and sources still pending
    full = copy.deepcopy(taxonomy)
    b = next(x for x in full["barriers"] if x["id"] == "B-F02")
    for cond, w in b["safe_followup_window_days"].items():
        w.update(days=w["days"] or 14, source="test guideline")
    assert "Safe follow-up window, whole calendar days from the planned discharge date: HF 7" in barrier_reference(full)
