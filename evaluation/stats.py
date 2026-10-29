"""Paired significance tests: the agentic pipeline against each baseline, per hypothesis.

Every system runs on the same cases, so each comparison is paired by case:

    primary family (pre-registered: the reference against B1 and B2)
    H1 barrier_recall           Wilcoxon signed-rank on per-case recall
    H2 task_recall              Wilcoxon signed-rank on per-case recall
    H3 plan_completeness        Wilcoxon signed-rank on per-case completeness
    H4 governance_compliance    Wilcoxon signed-rank on per-case compliance

    secondary family
    H4-strict governance_compliance_strict
                                exact McNemar test: a case is compliant only if
                                every run was (0 or 1)
    and every comparison with a system passed as ``secondary`` (none at present)

Each case contributes one value per system: the mean over the case's runs, the
same rule for every hypothesis. For H4 that is the share of the case's runs with
no governance violation (0, 1/3, 2/3, or 1 with three runs; 0 or 1 with one run,
where Wilcoxon reduces to a sign test on the discordant cases). Cases where
either system has nothing to count for a metric (a blank value in per_case.csv)
are left out of that comparison; n_pairs says how many remain.

Each row reports the means, the mean paired difference (reference - baseline)
with a 95% paired bootstrap interval, the test's p-value, a Holm-adjusted
p-value, and an effect size. Holm adjustment runs within each family: the
primary family (the pre-registered comparisons, e.g. against B1 and B2) and,
separately, the secondary family (H4-strict), so a secondary analysis never
changes a primary result. Effect sizes:

    rank_biserial   (W+ - W-) / (W+ + W-) over non-zero differences, from -1 to 1;
                    positive means the reference system scored higher
    risk_difference (H4-strict) strict compliance rate of the reference minus the baseline's

Wilcoxon drops zero differences (identical scores), which are common here, so a
comparison can have many pairs but few informative ones; n_nonzero shows that.
With fewer than 10 informative pairs the test has little power, and the row is
marked small_sample.

The default alternative is two-sided. The hypotheses are directional (agentic >
baselines), so --alternative greater is defensible if the team pre-registers it;
decide before looking at the results.
"""
from __future__ import annotations

import numpy as np
from scipy import stats

HYPOTHESES = [
    ("H1", "barrier_recall", "wilcoxon"),
    ("H2", "task_recall", "wilcoxon"),
    ("H3", "plan_completeness", "wilcoxon"),
    ("H4", "governance_compliance", "wilcoxon"),
]
STRICT = ("H4-strict", "governance_compliance_strict", "mcnemar")
SMALL_SAMPLE = 10


def per_case_values(rows: list[dict], system: str, metric: str) -> dict[str, float | None]:
    """case_id -> value of ``metric`` for ``system``, one value per case over its runs.

    governance_compliance is the share of the case's runs with no violations;
    governance_compliance_strict is 1 only if every run had none. Other metrics
    are the mean over the runs that have a value.
    """
    values = {}
    for r in rows:
        if r["system"] != system:
            continue
        v = (float(r["governance_violations"] == 0) if metric.startswith("governance_compliance")
             else r[metric])
        values.setdefault(r["case_id"], []).append(v)
    out = {}
    for case, vs in values.items():
        present = [v for v in vs if v is not None]
        if not present:
            out[case] = None
        elif metric == "governance_compliance_strict":
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
            [(b, STRICT, "secondary") for b in baselines] + \
            [(b, h, "secondary") for b in secondary for h in [*HYPOTHESES, STRICT]]
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
    return out
