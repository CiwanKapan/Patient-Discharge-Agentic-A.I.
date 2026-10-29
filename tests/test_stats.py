"""Tests for the paired significance tests in evaluation/stats.py."""
import numpy as np
import pytest

from evaluation import stats


def _rows(values: dict[str, list], metric="barrier_recall"):
    """per_case-style rows: {system: [value per case]}."""
    rows = []
    for system, vals in values.items():
        for i, v in enumerate(vals):
            row = {"system": system, "case_id": f"CASE-{i:03d}", "barrier_recall": None, "task_recall": None,
                   "plan_completeness": None, "governance_violations": 0}
            row[metric] = v
            rows.append(row)
    return rows


def test_holm_matches_hand_computation():
    assert stats.holm([0.01, 0.04, 0.03]) == pytest.approx([0.03, 0.06, 0.06])
    assert stats.holm([0.5, 0.9]) == pytest.approx([1.0, 1.0])


def test_wilcoxon_clear_win():
    ref, base = np.ones(12), np.full(12, 0.5)
    r = stats.wilcoxon(ref, base, "two-sided")
    assert r["n_nonzero"] == 12 and r["effect_size"] == 1.0
    assert r["p_value"] == pytest.approx(2 / 2**12)   # exact: all 12 signs positive


def test_wilcoxon_ignores_ties_and_reports_direction():
    ref = np.array([1, 1, 1, 0.5, 1.0])
    base = np.array([1, 1, 1, 1.0, 0.5])
    r = stats.wilcoxon(ref, base, "two-sided")
    assert r["n_nonzero"] == 2 and r["effect_size"] == 0.0
    assert stats.wilcoxon(np.ones(3), np.ones(3), "two-sided")["p_value"] == 1.0


def test_mcnemar_exact():
    ref = np.array([1] * 10 + [1] * 5)
    base = np.array([0] * 10 + [1] * 5)
    r = stats.mcnemar(ref, base, "two-sided")
    assert r["statistic"] == 10 and r["n_nonzero"] == 10
    assert r["p_value"] == pytest.approx(2 * 0.5**10)
    assert r["effect_size"] == pytest.approx(10 / 15)
    assert stats.mcnemar(ref, base, "greater")["p_value"] == pytest.approx(0.5**10)


def test_bootstrap_interval_brackets_the_mean():
    d = np.array([0.0, 0.2, 0.5, 0.1, 0.3])
    lo, hi = stats.bootstrap_ci(d)
    assert lo <= d.mean() <= hi
    assert stats.bootstrap_ci(d) == (lo, hi)  # seeded


def test_compare_skips_cases_with_nothing_to_count():
    rows = _rows({"Agentic": [1.0, None, 1.0], "B1": [0.5, 0.5, None]})
    out = stats.compare(rows, "Agentic", ["B1"])
    h1 = next(r for r in out if r["hypothesis"] == "H1")
    assert h1["n_pairs"] == 1
    h2 = next(r for r in out if r["hypothesis"] == "H2")
    assert h2["n_pairs"] == 0 and h2["p_value"] is None


def test_compare_flags_small_samples_and_adjusts():
    rows = _rows({"Agentic": [1.0] * 15, "B1": [0.5] * 15})
    out = stats.compare(rows, "Agentic", ["B1"])
    h1 = next(r for r in out if r["hypothesis"] == "H1")
    assert not h1["small_sample"] and h1["significant"]
    assert h1["p_holm"] >= h1["p_value"]
    h4 = next(r for r in out if r["hypothesis"] == "H4")
    assert h4["test"] == "wilcoxon" and h4["family"] == "primary" and h4["small_sample"]
    strict = next(r for r in out if r["hypothesis"] == "H4-strict")
    assert strict["test"] == "mcnemar_exact" and strict["family"] == "secondary"


def test_h4_primary_is_mean_compliance_and_strict_is_secondary():
    rows = []
    for system, violations in (("Agentic", [0, 0, 1]), ("B2", [0, 1, 1])):  # one case, three runs
        for run, v in enumerate(violations, 1):
            rows.append({"system": system, "case_id": "CASE-001", "run": f"r{run}", "barrier_recall": 1.0,
                         "task_recall": 1.0, "plan_completeness": 1.0, "governance_violations": v})
    assert stats.per_case_values(rows, "Agentic", "governance_compliance") == {"CASE-001": pytest.approx(2 / 3)}
    assert stats.per_case_values(rows, "Agentic", "governance_compliance_strict") == {"CASE-001": 0.0}
    out = stats.compare(rows, "Agentic", ["B2"])
    h4 = next(r for r in out if r["hypothesis"] == "H4")
    assert h4["mean_difference"] == pytest.approx(1 / 3)
    strict = next(r for r in out if r["hypothesis"] == "H4-strict")
    assert strict["mean_difference"] == 0.0  # both fail in some run, so strict sees no difference
    # Holm runs within families: the primary p-values ignore the secondary rows
    primary = [r for r in out if r["family"] == "primary" and r["p_value"] is not None]
    assert [r["p_holm"] for r in primary] == pytest.approx(stats.holm([r["p_value"] for r in primary]))
    assert {r["hypothesis"] for r in out if r["family"] == "primary"} == {"H1", "H2", "H3", "H4"}


def test_governance_compliance_comes_from_violations():
    rows = _rows({"Agentic": [1.0, 1.0], "B2": [1.0, 1.0]})
    rows[2]["governance_violations"] = 2
    assert stats.per_case_values(rows, "B2", "governance_compliance") == {"CASE-000": 0.0, "CASE-001": 1.0}
