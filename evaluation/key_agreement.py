"""Agreement between independent annotators and the generated answer keys (pre-registration Amendment 10).

    python -m evaluation.key_agreement data/key_reviews/independent_check/annotations.csv

The annotations CSV has one row per annotated item:
    annotator, case_id, item_type (barrier | information_gap | task), item_id, evidence, notes

For each item type, every (case, ID) pair the taxonomy allows for the case's condition is a yes/no judgment:
does the annotator (or key) list it? Agreement is computed over those pairs, pooled across the cases:

    kappa           Cohen's kappa
    positive_agreement  2a / (2a + b + c): agreement on the items either side listed (an F1)
    observed        share of all pairs on which they agree (inflated by the many absent IDs; reported only)

Rows: each annotator against the generated key, and each pair of annotators. disagreements.csv lists every
(case, item) the two sides judged differently, for adjudication.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.pipeline._common import load_taxonomy  # noqa: E402
from src.utils.run_records import case_path, key_path  # noqa: E402

ITEM_TYPES = ("barrier", "information_gap", "task")


def universe(taxonomy: dict, condition: str, item_type: str) -> set[str]:
    pool = taxonomy["tasks"] if item_type == "task" else taxonomy["barriers"]
    return {x["id"] for x in pool if condition in x["conditions"]}


def key_items(case_id: str) -> dict[str, set[str]]:
    k = json.loads(key_path(case_id).read_text())
    return {"barrier": {b["barrier_id"] for b in k["barriers"]},
            "information_gap": {g["candidate_barrier_id"] for g in k["information_gaps"]},
            "task": {t["task_id"] for t in k["tasks"]}}


def read_annotations(path: Path) -> dict[str, dict[str, dict[str, set[str]]]]:
    """annotator -> case_id -> item_type -> IDs."""
    out: dict = defaultdict(lambda: defaultdict(lambda: {t: set() for t in ITEM_TYPES}))
    for r in csv.DictReader(Path(path).open()):
        who, cid, kind, item = (r.get(k, "").strip() for k in ("annotator", "case_id", "item_type", "item_id"))
        if not (who and cid and item):
            continue
        if kind not in ITEM_TYPES:
            raise SystemExit(f"unknown item_type {kind!r} for {cid}; use one of {ITEM_TYPES}")
        out[who][cid][kind].add(item)
    return out


def agreement(pairs: list[tuple[bool, bool]]) -> dict:
    a = sum(x and y for x, y in pairs)
    b = sum(x and not y for x, y in pairs)
    c = sum(y and not x for x, y in pairs)
    d = sum(not x and not y for x, y in pairs)
    n = a + b + c + d
    if not n:
        return {"n": 0, "kappa": None, "positive_agreement": None, "observed": None}
    po = (a + d) / n
    pe = ((a + b) * (a + c) + (c + d) * (b + d)) / n ** 2
    return {"n": n, "both": a, "only_first": b, "only_second": c,
            "kappa": None if pe == 1 else (po - pe) / (1 - pe),
            "positive_agreement": 2 * a / (2 * a + b + c) if a + b + c else None,
            "observed": po}


def compare(first: dict, second: dict, cases: list[str], taxonomy: dict, conditions: dict):
    rows, disagreements = [], []
    for kind in ITEM_TYPES:
        pairs = []
        for cid in cases:
            for item in sorted(universe(taxonomy, conditions[cid], kind)):
                x, y = item in first[cid][kind], item in second[cid][kind]
                pairs.append((x, y))
                if x != y:
                    disagreements.append((cid, kind, item, x, y))
        rows.append({"item_type": kind, **agreement(pairs)})
    return rows, disagreements


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="python -m evaluation.key_agreement", description=__doc__.split("\n")[0])
    p.add_argument("annotations", type=Path)
    p.add_argument("--out", type=Path, help="default: next to the annotations file")
    a = p.parse_args(argv)
    taxonomy = load_taxonomy()
    ann = read_annotations(a.annotations)
    if not ann:
        p.error("no annotations found")
    cases = sorted({cid for by_case in ann.values() for cid in by_case})
    conditions = {cid: json.loads(case_path(cid).read_text())["condition"] for cid in cases}
    sources = {"key": {cid: key_items(cid) for cid in cases},
               **{who: {cid: by_case.get(cid, {t: set() for t in ITEM_TYPES}) for cid in cases}
                  for who, by_case in ann.items()}}
    results, disagreements = [], []
    for first, second in [("key", w) for w in ann] + list(itertools.combinations(sorted(ann), 2)):
        rows, dis = compare(sources[first], sources[second], cases, taxonomy, conditions)
        results += [{"first": first, "second": second, **r} for r in rows]
        disagreements += [{"first": first, "second": second, "case_id": c, "item_type": k, "item_id": i,
                           "listed_by_first": x, "listed_by_second": y} for c, k, i, x, y in dis]
    out = a.out or a.annotations.parent
    out.mkdir(parents=True, exist_ok=True)
    for name, rows in (("agreement.csv", results), ("disagreements.csv", disagreements)):
        if rows:
            with open(out / name, "w", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=list(rows[0]))
                w.writeheader()
                w.writerows(rows)
    print(f"{len(cases)} cases, annotators: {', '.join(sorted(ann))}")
    print(f"{'first':<10}{'second':<12}{'items':<17}{'pairs':>6}{'kappa':>8}{'pos.agr':>9}{'observed':>10}")
    fmt = lambda v: "-" if v is None else f"{v:.3f}"  # noqa: E731
    for r in results:
        print(f"{r['first']:<10}{r['second']:<12}{r['item_type']:<17}{r['n']:>6}{fmt(r['kappa']):>8}"
              f"{fmt(r['positive_agreement']):>9}{fmt(r['observed']):>10}")
    print(f"\nwrote {out / 'agreement.csv'} and {out / 'disagreements.csv'} ({len(disagreements)} disagreements)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
