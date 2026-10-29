"""Write the case subsets used by scripts/run_experiment.py, from a fixed seed.

    python scripts/make_subsets.py

data/subsets/stratified_40.txt
    40 cases for the reduced design (1 run on all cases, 3 runs on these):
    exactly 8 per condition and 12/20/8 easy/medium/hard (the dataset's 30/50/20).
    Each condition gets its share of each difficulty rounded down; the cases
    left over go to seeded conditions, one per condition, so both totals hold.

The pilot does not use a subset of the evaluation cases: it runs the separate
development set (data/dev/, scripts/generate_cases.py --dev).
"""
from __future__ import annotations

import csv
import random
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED = 20261030


def cells() -> dict[tuple[str, str], list[str]]:
    out = defaultdict(list)
    for r in csv.DictReader((ROOT / "data" / "dataset_manifest.csv").open()):
        out[(r["condition"], r["difficulty"])].append(r["case_id"])
    return {k: sorted(v) for k, v in sorted(out.items())}


def stratified(n: int, groups: dict, rng: random.Random) -> list[str]:
    conds = sorted({c for c, _ in groups})
    diffs = ["easy", "medium", "hard"]
    sizes = {d: sum(len(v) for (_, dd), v in groups.items() if dd == d) for d in diffs}
    total = sum(sizes.values())
    per_cond = n // len(conds)
    diff_total = {d: round(n * sizes[d] / total) for d in diffs}
    take = {(c, d): int(per_cond * sizes[d] / total) for c in conds for d in diffs}
    short = [d for d in diffs for _ in range(diff_total[d] - sum(take[(c, d)] for c in conds))]
    order = conds[:]
    rng.shuffle(order)
    for c, d in zip((c for c in order for _ in range(per_cond - sum(take[(c, x)] for x in diffs))), short):
        take[(c, d)] += 1
    assert sum(take.values()) == n
    return sorted(x for k, v in groups.items() for x in rng.sample(v, take[k]))


def main() -> None:
    groups = cells()
    out = ROOT / "data" / "subsets"
    out.mkdir(parents=True, exist_ok=True)
    subset = stratified(40, groups, random.Random(SEED))
    header = f"# written by scripts/make_subsets.py (seed {SEED}); one case ID per line\n"
    (out / "stratified_40.txt").write_text(header + "\n".join(subset) + "\n")
    print(f"wrote {len(subset)} cases to stratified_40.txt")


if __name__ == "__main__":
    main()
