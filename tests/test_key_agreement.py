"""The independent key check: subset selection, blinding, and agreement statistics."""
import csv
import json

import pytest

from evaluation import key_agreement as ka
from scripts import make_key_review_materials as mk
from src.utils.run_records import key_path


def _write(tmp_path, rows):
    p = tmp_path / "annotations.csv"
    with open(p, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["annotator", "case_id", "item_type", "item_id", "evidence", "notes"])
        w.writerows(rows)
    return p


def _rows_from_key(who, cid):
    k = json.loads(key_path(cid).read_text())
    return ([[who, cid, "barrier", b["barrier_id"], "", ""] for b in k["barriers"]]
            + [[who, cid, "information_gap", g["candidate_barrier_id"], "", ""] for g in k["information_gaps"]]
            + [[who, cid, "task", t["task_id"], "", ""] for t in k["tasks"]])


def test_kappa_matches_hand_computation():
    # 2x2: both 2, only_first 1, only_second 1, neither 6 -> po 0.8, pe 0.58, kappa 0.5238
    pairs = [(True, True)] * 2 + [(True, False)] + [(False, True)] + [(False, False)] * 6
    r = ka.agreement(pairs)
    assert r["observed"] == pytest.approx(0.8)
    assert r["kappa"] == pytest.approx((0.8 - 0.58) / 0.42)
    assert r["positive_agreement"] == pytest.approx(4 / 6)


def test_annotator_identical_to_the_key_agrees_perfectly(tmp_path, capsys):
    cases = ["CASE-151", "CASE-152", "CASE-154"]
    path = _write(tmp_path, [row for c in cases for row in _rows_from_key("ann1", c)])
    assert ka.main([str(path)]) == 0
    rows = list(csv.DictReader((tmp_path / "agreement.csv").open()))
    barrier = next(r for r in rows if r["item_type"] == "barrier")
    assert float(barrier["kappa"]) == 1.0 and float(barrier["positive_agreement"]) == 1.0
    assert not (tmp_path / "disagreements.csv").exists()


def test_disagreements_are_listed_and_annotator_pairs_compared(tmp_path):
    a1 = _rows_from_key("ann1", "CASE-151")
    a2 = [r for r in _rows_from_key("ann2", "CASE-151") if not (r[2] == "barrier" and r[3] == "B-E07")]
    path = _write(tmp_path, a1 + a2 + [["ann2", "CASE-151", "barrier", "B-S02", "", ""]])
    ka.main([str(path)])
    rows = list(csv.DictReader((tmp_path / "agreement.csv").open()))
    assert {(r["first"], r["second"]) for r in rows} == {("key", "ann1"), ("key", "ann2"), ("ann1", "ann2")}
    dis = list(csv.DictReader((tmp_path / "disagreements.csv").open()))
    assert {(d["second"], d["item_id"]) for d in dis if d["first"] == "key"} == {("ann2", "B-E07"), ("ann2", "B-S02")}


def test_subset_is_stratified_and_covers_the_hard_parts():
    rows = mk.manifest_rows()
    ids = mk.choose_subset(rows)
    assert len(ids) == 20 and len(set(ids)) == 20
    from collections import Counter
    assert Counter(rows[c]["condition"] for c in ids) == {c: 4 for c in mk.CONDS}
    assert Counter(rows[c]["difficulty"] for c in ids) == {"easy": 6, "medium": 10, "hard": 4}
    assert mk.covered(ids, rows)
    assert ids == mk.choose_subset(rows)  # seeded


def test_blinded_page_shows_no_key_or_labels():
    from src.models.case import PatientCase
    from src.utils.run_records import case_path
    case = PatientCase.model_validate_json(case_path("CASE-151").read_text())
    page = mk.render_case(case)
    assert "Answer key" not in page and "Must not flag" not in page
    assert '"difficulty"' not in page and "hard" not in page.split("\n")[0]
    assert "## Tracked fields" in page and "## Free-text notes" in page
