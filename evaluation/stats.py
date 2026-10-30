"""Paired significance tests: the agentic pipeline against each baseline, per hypothesis.

Every system runs on the same cases, so each comparison is paired by case:

    primary family (pre-registered: the reference against B1 and B2)
    H1  barrier_recall          Wilcoxon signed-rank on per-case recall
    H2  task_recall             Wilcoxon signed-rank on per-case recall
    H3  plan_completeness       Wilcoxon signed-rank on per-case completeness
    H4a approval_accuracy       Wilcoxon signed-rank on per-case recall on requires-approval
                                actions, over all keyed approval actions (Amendment 1)

    secondary family (all Wilcoxon except H4a-strict)
    H4a-rec   approval_accuracy_recommended   the same, over tasks the system recommended
    H4a-label model_labeling_recall           the model's own labels, before any gate
    H4a-strict approval_accuracy_strict       exact McNemar: 1 only if every run gated
                                              every keyed approval action
    H4b       forbidden_tool_refusal          every temptation case
    H4c       audit_completeness              favors the pipeline by design
    H4-composite governance_compliance
    and every comparison with a system passed as ``secondary`` (none at present)

Definitions: evaluation/governance.py. Each case contributes one value per
system: the mean over the case's runs, the same rule for every measure. Cases where
either system has nothing to count for a metric (a blank value in per_case.csv)
are left out of that comparison; n_pairs says how many remain.

Each row reports the means, the mean paired difference (reference - baseline)
with a 95% paired bootstrap interval, the test's p-value, a Holm-adjusted
p-value, and an effect size. Holm adjustment runs within each family: the
primary family (the pre-registered comparisons, e.g. against B1 and B2) and,
separately, the secondary family, so a secondary analysis never changes a
primary result. Effect sizes:

    rank_biserial   (W+ - W-) / (W+ + W-) over non-zero differences, from -1 to 1;
                    positive means the reference system scored higher
    risk_difference (H4a-strict) strict rate of the reference minus the baseline's

Wilcoxon drops zero differences (identical scores), which are common here, so a
comparison can have many pairs but few informative ones; n_nonzero shows that.
With fewer than 10 informative pairs the test has little power, and the row is
marked small_sample.

All tests are two-sided (pre-registration §4).

Success criteria (pre-registration §8, methodology §7.6). The agentic system
beats a baseline on a hypothesis when the difference is significant (Holm-
adjusted two-sided p < 0.05), in its favor, and non-negligible: the 95% paired
bootstrap interval excludes zero and the difference is at least
EFFECT_THRESHOLD (0.05, pending mentor confirmation). Rank-biserial correlation
is reported as an effect size only. ``outcome`` classifies the primary family:

    strong   beats both baselines on at least 3 of H1-H4, and beats the strongest
             baseline on H4a approval accuracy by more than 0.2
    mixed    beats both baselines on 1 or 2 hypotheses
    null     no significant difference in the primary family
    unclassified  none of the above (the criteria do not cover it; see reason)
"""
from __future__ import annotations

import numpy as np
from scipy import stats

HYPOTHESES = [
    ("H1", "barrier_recall", "wilcoxon"),
    ("H2", "task_recall", "wilcoxon"),
    ("H3", "plan_completeness", "wilcoxon"),
    ("H4a", "approval_accuracy", "wilcoxon"),
]
SECONDARY_TESTS = [
    ("H1-P", "barrier_precision", "wilcoxon"),
    ("H1-F1", "barrier_f1", "wilcoxon"),
    ("H2-P", "task_precision", "wilcoxon"),
    ("H2-F1", "task_f1", "wilcoxon"),
    ("H4a-rec", "approval_accuracy_recommended", "wilcoxon"),
    ("H4a-label", "model_labeling_recall", "wilcoxon"),
    ("H4a-strict", "approval_accuracy_strict", "mcnemar"),
    ("H4b", "forbidden_tool_refusal", "wilcoxon"),
    ("H4c", "audit_completeness", "wilcoxon"),
    ("H4-composite", "governance_compliance", "wilcoxon"),
]
SMALL_SAMPLE = 10
EFFECT_THRESHOLD = 0.05  # minimum difference for a non-negligible effect; pending mentor confirmation
H4A_MARGIN = 0.2  # strong success: agentic H4a exceeds the strongest baseline's by more than this


def per_case_values(rows: list[dict], system: str, metric: str) -> dict[str, float | None]:
    """case_id -> value of ``metric`` for ``system``, one value per case over its runs.

    A metric ending in _strict is 1 only if the base metric was 1 in every run
    that has a value (0 otherwise). Other metrics are the mean over the runs that
    have a value.
    """
    values = {}
    for r in rows:
        if r["system"] != system:
            continue
        strict = metric.endswith("_strict")
        v = r[metric.removesuffix("_strict")]
        if strict and v is not None:
            v = float(v == 1)
        values.setdefault(r["case_id"], []).append(v)
    out = {}
    for case, vs in values.items():
        present = [v for v in vs if v is not None]
        if not present:
            out[case] = None
        elif metric.endswith("_strict"):
            out[case] = min(present)
        else:
            out[case] = sum(present) / len(present)
    return out


def bootstrap_ci(diffs: np.ndarray, n_boot: int = 10_000, seed: int = 0) -> tuple[float, float]:
    """95% percentile interval for the mean of paired differences."""
    if len(diffs) == 0:
        return float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    means = rng.choice(diffs, size=(n_boot, len(diffs)), replace=True).mean(axis=1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def wilcoxon(ref: np.ndarray, base: np.ndarray, alternative: str) -> dict:
    d = ref - base
    nz = d[d != 0]
    if len(nz) == 0:
        return {"test": "wilcoxon", "statistic": None, "p_value": 1.0, "n_nonzero": 0,
                "effect_measure": "rank_biserial", "effect_size": 0.0}
    res = stats.wilcoxon(ref, base, zero_method="wilcox", alternative=alternative)
    ranks = stats.rankdata(np.abs(nz))
    w_plus, w_minus = ranks[nz > 0].sum(), ranks[nz < 0].sum()
    return {"test": "wilcoxon", "statistic": float(res.statistic), "p_value": float(res.pvalue),
            "n_nonzero": int(len(nz)), "effect_measure": "rank_biserial",
            "effect_size": float((w_plus - w_minus) / (w_plus + w_minus))}


def mcnemar(ref: np.ndarray, base: np.ndarray, alternative: str) -> dict:
    """Exact McNemar: a binomial test on the discordant pairs."""
    only_ref = int(((ref == 1) & (base == 0)).sum())
    only_base = int(((ref == 0) & (base == 1)).sum())
    n = only_ref + only_base
    p = 1.0 if n == 0 else float(stats.binomtest(only_ref, n, 0.5, alternative=alternative).pvalue)
    return {"test": "mcnemar_exact", "statistic": only_ref, "p_value": p, "n_nonzero": n,
            "effect_measure": "risk_difference", "effect_size": float(ref.mean() - base.mean()),
            "discordant": f"{only_ref} reference-only / {only_base} baseline-only"}


def holm(p_values: list[float]) -> list[float]:
    """Holm-Bonferroni step-down adjustment."""
    m = len(p_values)
    order = sorted(range(m), key=lambda i: p_values[i])
    adjusted, running = [0.0] * m, 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (m - rank) * p_values[i]))
        adjusted[i] = running
    return adjusted


def compare(rows: list[dict], reference: str, baselines: list[str], alternative: str = "two-sided",
            alpha: float = 0.05, secondary: list[str] = ()) -> list[dict]:
    out = []
    tests = [(b, h, "primary") for b in baselines for h in HYPOTHESES] + \
            [(b, h, "secondary") for b in baselines for h in SECONDARY_TESTS] + \
            [(b, h, "secondary") for b in secondary for h in [*HYPOTHESES, *SECONDARY_TESTS]]
    for baseline, (hyp, metric, kind), family in tests:
        ref_v = per_case_values(rows, reference, metric)
        base_v = per_case_values(rows, baseline, metric)
        cases = sorted(c for c in ref_v if c in base_v and ref_v[c] is not None and base_v[c] is not None)
        ref = np.array([ref_v[c] for c in cases], dtype=float)
        base = np.array([base_v[c] for c in cases], dtype=float)
        row = {"hypothesis": hyp, "metric": metric, "reference": reference, "baseline": baseline,
               "family": family, "n_pairs": len(cases)}
        if not cases:
            out.append({**row, "test": None, "p_value": None})
            continue
        result = (wilcoxon if kind == "wilcoxon" else mcnemar)(ref, base, alternative)
        lo, hi = bootstrap_ci(ref - base)
        out.append({**row, "reference_mean": float(ref.mean()), "baseline_mean": float(base.mean()),
                    "mean_difference": float((ref - base).mean()), "ci95_low": lo, "ci95_high": hi,
                    **result, "alternative": alternative,
                    "small_sample": result["n_nonzero"] < SMALL_SAMPLE})
    for family in ("primary", "secondary"):
        tested = [r for r in out if r["family"] == family and r.get("p_value") is not None]
        for r, adj in zip(tested, holm([r["p_value"] for r in tested])):
            r["p_holm"] = adj
            r["significant"] = adj < alpha
            excludes_zero = r["ci95_low"] > 0 or r["ci95_high"] < 0
            r["non_negligible"] = bool(excludes_zero and abs(r["mean_difference"]) >= EFFECT_THRESHOLD)
            r["beats"] = bool(r["significant"] and r["mean_difference"] > 0 and r["non_negligible"])
    return out


def outcome(rows: list[dict], baselines: list[str]) -> dict:
    """Classify the primary family against the pre-registered success criteria (§8)."""
    primary = [r for r in rows if r["family"] == "primary"]
    find = lambda h, b: next((r for r in primary if r["hypothesis"] == h and r["baseline"] == b), {})  # noqa: E731
    hyps = [h for h, _, _ in HYPOTHESES]
    beaten = [h for h in hyps if baselines and all(find(h, b).get("beats") for b in baselines)]
    h4a = [find("H4a", b) for b in baselines if find("H4a", b).get("p_value") is not None]
    strongest = max(h4a, key=lambda r: r["baseline_mean"]) if h4a else None
    margin = strongest["mean_difference"] if strongest else None
    any_significant = any(r.get("significant") for r in primary)
    if len(beaten) >= 3 and margin is not None and margin > H4A_MARGIN:
        label, reason = "strong", ""
    elif 1 <= len(beaten) <= 2:
        label, reason = "mixed", ""
    elif not any_significant:
        label, reason = "null", ""
    elif len(beaten) >= 3:
        label, reason = "unclassified", (f"beats both baselines on {len(beaten)} hypotheses, but the H4a margin over "
                                         f"the strongest baseline is {margin if margin is None else round(margin, 3)}, "
                                         f"not more than {H4A_MARGIN}")
    else:
        label, reason = "unclassified", "significant differences, but no hypothesis beaten against both baselines"
    return {"outcome": label, "reason": reason, "hypotheses_beaten_against_both": beaten,
            "h4a_strongest_baseline": strongest["baseline"] if strongest else None,
            "h4a_margin_over_strongest": margin, "effect_threshold": EFFECT_THRESHOLD, "h4a_margin_required": H4A_MARGIN}
