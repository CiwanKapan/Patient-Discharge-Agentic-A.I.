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
                   "barrier_precision": None, "barrier_f1": None, "task_precision": None, "task_f1": None,
                   "plan_completeness": None, "approval_accuracy": None, "approval_accuracy_recommended": None,
                   "model_labeling_recall": None, "forbidden_tool_refusal": None, "audit_completeness": 1,
                   "governance_compliance": 1}
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
    assert [r["hypothesis"] for r in out if r["family"] == "primary"] == ["H1", "H2", "H3", "H4a"]
    strict = next(r for r in out if r["hypothesis"] == "H4a-strict")
    assert strict["family"] == "secondary" and strict["n_pairs"] == 0  # no approval data in these rows


def test_h4a_is_primary_and_the_rest_of_h4_is_secondary():
    rows = []
    for system, acc in (("Agentic", [1.0, 1.0, 0.5]), ("B2", [1.0, 0.5, 0.5])):  # one case, three runs
        for run, a in enumerate(acc, 1):
            rows.append({"system": system, "case_id": "CASE-001", "run": f"r{run}", "barrier_recall": 1.0,
                         "barrier_precision": 1.0, "barrier_f1": 1.0, "task_precision": 1.0, "task_f1": 1.0,
                         "task_recall": 1.0, "plan_completeness": 1.0, "approval_accuracy": a,
                         "approval_accuracy_recommended": 1.0, "model_labeling_recall": a,
                         "forbidden_tool_refusal": None, "audit_completeness": int(system == "Agentic"),
                         "governance_compliance": int(system == "Agentic" and a == 1.0)})
    assert stats.per_case_values(rows, "Agentic", "approval_accuracy") == {"CASE-001": pytest.approx(5 / 6)}
    assert stats.per_case_values(rows, "Agentic", "approval_accuracy_strict") == {"CASE-001": 0.0}
    out = stats.compare(rows, "Agentic", ["B2"])
    h4a = next(r for r in out if r["hypothesis"] == "H4a")
    assert h4a["family"] == "primary" and h4a["mean_difference"] == pytest.approx(1 / 6)
    assert [r["hypothesis"] for r in out if r["family"] == "secondary"] == [
        "H1-P", "H1-F1", "H2-P", "H2-F1", "H4a-rec", "H4a-label", "H4a-strict", "H4b", "H4c", "H4-composite"]
    assert next(r for r in out if r["hypothesis"] == "H4b")["n_pairs"] == 0  # never scored here
    primary = [r for r in out if r["family"] == "primary" and r["p_value"] is not None]
    assert [r["p_holm"] for r in primary] == pytest.approx(stats.holm([r["p_value"] for r in primary]))


# ---------------------------------------------------------------- success criteria (pre-registration §8)
def test_beats_needs_significance_direction_and_a_non_negligible_effect():
    rows = _rows({"Agentic": [1.0] * 15, "B1": [0.5] * 15})
    h1 = next(r for r in stats.compare(rows, "Agentic", ["B1"]) if r["hypothesis"] == "H1")
    assert h1["significant"] and h1["non_negligible"] and h1["beats"]
    tiny = _rows({"Agentic": [1.0] * 15, "B1": [0.98] * 15})  # significant and CI excludes 0, but diff < 0.05
    h1 = next(r for r in stats.compare(tiny, "Agentic", ["B1"]) if r["hypothesis"] == "H1")
    assert h1["significant"] and not h1["non_negligible"] and not h1["beats"]
    worse = _rows({"Agentic": [0.5] * 15, "B1": [1.0] * 15})  # significant, non-negligible, wrong direction
    h1 = next(r for r in stats.compare(worse, "Agentic", ["B1"]) if r["hypothesis"] == "H1")
    assert h1["significant"] and h1["non_negligible"] and not h1["beats"]


def _primary(beats: dict, h4a_margin=0.3, significant=None, reversals=()):
    """Synthetic primary-family rows: beats[(hypothesis, baseline)] -> bool."""
    rows = []
    for (h, b), win in beats.items():
        rows.append({"hypothesis": h, "baseline": b, "family": "primary", "p_value": 0.01,
                     "significant": win if significant is None else significant, "beats": win,
                     "reversal": (h, b) in reversals,
                     "mean_difference": h4a_margin if h == "H4a" else 0.1,
                     "baseline_mean": {"B1": 0.3, "B2": 0.7}[b]})
    return rows


@pytest.mark.parametrize("wins, margin, significant, expected", [
    ({"H1", "H2", "H3", "H4a"}, 0.3, None, "strong"),
    ({"H1", "H2", "H4a"}, 0.25, None, "strong"),
    ({"H1", "H2", "H3"}, 0.1, None, "mixed"),       # 3 beaten, H4a margin not > 0.2
    ({"H1", "H2", "H3", "H4a"}, 0.2, None, "mixed"),  # margin must be MORE than 0.2
    ({"H1", "H4a"}, 0.3, None, "mixed"),
    ({"H2"}, 0.0, None, "mixed"),
    (set(), 0.0, False, "null"),
    (set(), 0.0, True, "null"),                       # significant somewhere, nothing beaten against both
])
def test_outcome_labels_are_exhaustive(wins, margin, significant, expected):
    beats = {(h, b): h in wins for h in ("H1", "H2", "H3", "H4a") for b in ("B1", "B2")}
    result = stats.outcome(_primary(beats, margin, significant), ["B1", "B2"])
    assert result["outcome"] == expected
    assert result["h4a_strongest_baseline"] == "B2"  # the baseline with the higher H4a
    assert result["reversal"] is False


def test_every_combination_gets_one_of_the_three_labels():
    import itertools
    hyps = ("H1", "H2", "H3", "H4a")
    for pattern in itertools.product([False, True], repeat=8):
        beats = dict(zip(((h, b) for h in hyps for b in ("B1", "B2")), pattern))
        for margin in (0.1, 0.3):
            assert stats.outcome(_primary(beats, margin), ["B1", "B2"])["outcome"] in ("strong", "mixed", "null")


def test_reversal_flag_is_raised_whatever_the_label():
    beats = {(h, b): b == "B1" or h == "H1" for h in ("H1", "H2", "H3", "H4a") for b in ("B1", "B2")}
    result = stats.outcome(_primary(beats, 0.3, reversals={("H3", "B2")}), ["B1", "B2"])
    assert result["outcome"] == "mixed" and result["reversal"] is True
    assert result["reversals"] == ["B2 beats the agentic system on H3"]


def test_reversal_needs_significance_and_a_non_negligible_effect():
    worse = _rows({"Agentic": [0.5] * 15, "B1": [1.0] * 15})
    h1 = next(r for r in stats.compare(worse, "Agentic", ["B1"]) if r["hypothesis"] == "H1")
    assert h1["reversal"] and not h1["beats"]
    slightly = _rows({"Agentic": [0.98] * 15, "B1": [1.0] * 15})  # significant, but diff < 0.05
    h1 = next(r for r in stats.compare(slightly, "Agentic", ["B1"]) if r["hypothesis"] == "H1")
    assert not h1["reversal"]


def test_a_hypothesis_counts_only_when_beaten_against_both_baselines():
    beats = {(h, b): True for h in ("H1", "H2", "H3", "H4a") for b in ("B1", "B2")}
    beats[("H2", "B2")] = beats[("H3", "B2")] = False
    result = stats.outcome(_primary(beats, 0.3), ["B1", "B2"])
    assert result["hypotheses_beaten_against_both"] == ["H1", "H4a"] and result["outcome"] == "mixed"
