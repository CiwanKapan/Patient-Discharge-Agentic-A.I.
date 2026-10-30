"""Write the answer-key review materials (no model calls).

    python scripts/make_key_review_materials.py

data/key_reviews/independent_check/   the 20-case independent key check (pre-registration Amendment 10)
    cases.txt              20 evaluation cases, seeded and stratified: 4 per condition, 6/10/4 easy/medium/hard,
                           with coverage of cross-field, note-only, information-gap, near-miss, and temptation cases
    packet/CASE-###.md     each case exactly as the models see it: NO answer key, difficulty, or distractor labels
    reference.md           the taxonomy and chart-reading rules the annotators work from (what the models get)
    annotations_template.csv
data/key_reviews/full_review/          the review of all 160 keys before the run (review packet item 12, option A)
    CASE-###.md            the case and its answer key side by side
    review_sheet.csv       one row per case for the reviewer's decision

Annotators for the independent check must not see the full-review pages, which show the keys.
"""
from __future__ import annotations

import csv
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.models.case import PatientCase  # noqa: E402
from src.models.plan import task_approval  # noqa: E402
from src.pipeline._common import CHART_READING_RULES, barrier_reference, case_view, load_taxonomy, task_reference  # noqa: E402
from src.utils.run_records import CASE_SETS, case_files  # noqa: E402

OUT = ROOT / "data" / "key_reviews"
SEED = 20261031
CONDS = ("HF", "CO", "PN", "OR", "ST")


def manifest_rows() -> dict[str, dict]:
    return {r["case_id"]: r for r in csv.DictReader(CASE_SETS["eval"][2].open())}


def covered(ids: list[str], rows: dict) -> bool:
    count = lambda col: sum(bool(rows[c][col]) for c in ids)  # noqa: E731
    return (count("cross_field_barriers") >= 3 and count("note_only_barriers") >= 3 and count("information_gaps") >= 3
            and count("near_miss_controls") >= 2 and count("forbidden_temptation") >= 2
            and count("approval_actions_expected") >= 5)


def choose_subset(rows: dict, seed: int = SEED) -> list[str]:
    """4 per condition; 2 medium each; one condition gets 2 easy, the rest 1 easy + 1 hard (6/10/4 overall).
    Redrawn from the same seed until the coverage minimums hold."""
    cells = defaultdict(list)
    for cid, r in sorted(rows.items()):
        cells[(r["condition"], r["difficulty"])].append(cid)
    rng = random.Random(seed)
    for _ in range(10_000):
        two_easy = rng.choice(CONDS)
        picks = []
        for cond in CONDS:
            plan = {"easy": 2, "medium": 2, "hard": 0} if cond == two_easy else {"easy": 1, "medium": 2, "hard": 1}
            for diff, n in plan.items():
                picks += rng.sample(cells[(cond, diff)], n)
        if covered(picks, rows):
            return sorted(picks)
    raise RuntimeError("no stratified subset met the coverage minimums")


def render_case(case: PatientCase) -> str:
    """The case as the models see it (case_view: no difficulty or distractor labels), made readable."""
    v = json.loads(case_view(case))
    lines = [f"# {v['case_id']} — condition {v['condition']}", ""]
    w = v.get("planned_discharge_window")
    lines += [f"**Planned discharge window:** {w['start']} to {w['end']}" if w else "**Planned discharge window:** not documented", ""]
    lines += ["## Tracked fields", "", "| Field | Status | Details |", "|---|---|---|"]
    for name, f in v.get("tracked_fields", {}).items():
        extra = "; ".join(f"{k}: {val}" for k, val in f.items() if k != "status")
        lines.append(f"| {name} | {f.get('status')} | {extra.replace('|', '/')} |")
    lines += ["", "(A field not listed is undocumented.)", "", "## Free-text notes", ""]
    for note, text in v.get("free_text_notes", {}).items():
        lines += [f"**{note}**", "", text, ""]
    if v.get("policy_context"):
        lines += ["## Policy context", "", "```", json.dumps(v["policy_context"], indent=1), "```", ""]
    return "\n".join(lines)


def render_key(key: dict, taxonomy: dict) -> str:
    lines = ["## Answer key (generated draft)", ""]
    lines += ["**Barriers**", ""] + ([f"- {b['barrier_id']} ({'cross-field' if b['cross_field'] else 'single-field'}) — "
                                     f"evidence: {', '.join(b['evidence_fields'])}" for b in key["barriers"]] or ["- none"])
    lines += ["", "**Information gaps**", ""] + ([f"- {g['field']} → could indicate {g['candidate_barrier_id']}"
                                                  for g in key["information_gaps"]] or ["- none"])
    lines += ["", "**Tasks**", ""]
    for t in key["tasks"] or []:
        rule = task_approval(taxonomy, t["task_id"])
        lines.append(f"- {t['task_id']} resolves {', '.join(t['resolves'])}"
                     + (f" — needs sign-off {rule['id']} ({rule['action']})" if rule else ""))
    if not key["tasks"]:
        lines.append("- none")
    lines += ["", f"**Must not flag (negative controls):** {', '.join(key['must_not_flag']) or 'none'}", ""]
    return "\n".join(lines)


def main() -> None:
    taxonomy = load_taxonomy()
    rows = manifest_rows()
    case_dir, key_dir, _ = CASE_SETS["eval"]

    # ---------------- independent check (blinded)
    ic = OUT / "independent_check"
    (ic / "packet").mkdir(parents=True, exist_ok=True)
    subset = choose_subset(rows)
    (ic / "cases.txt").write_text(f"# 20-case independent key check (scripts/make_key_review_materials.py, seed {SEED})\n"
                                  + "\n".join(subset) + "\n")
    for cid in subset:
        case = PatientCase.model_validate_json((case_dir / f"{cid}.json").read_text())
        (ic / "packet" / f"{cid}.md").write_text(render_case(case))
    (ic / "reference.md").write_text(
        "# Reference for annotators\n\nThis is the taxonomy and the chart-reading rules the systems receive. "
        "Use only IDs listed here, and only those whose conditions include the case's condition.\n\n"
        f"## Barriers\n\n{barrier_reference(taxonomy)}\n\n## Tasks\n\n{task_reference(taxonomy)}\n\n{CHART_READING_RULES}\n")
    with open(ic / "annotations_template.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["annotator", "case_id", "item_type", "item_id", "evidence", "notes"])
        for cid in subset:
            w.writerow(["", cid, "barrier | information_gap | task", "", "", ""])

    # ---------------- full review (keys visible)
    fr = OUT / "full_review"
    fr.mkdir(parents=True, exist_ok=True)
    sheet = []
    for p in case_files(case_dir):
        case = PatientCase.model_validate_json(p.read_text())
        key = json.loads((key_dir / f"{p.stem}.key.json").read_text())
        r = rows[p.stem]
        (fr / f"{p.stem}.md").write_text(render_case(case) + "\n---\n\n" + render_key(key, taxonomy))
        sheet.append({"case_id": p.stem, "condition": r["condition"], "difficulty": r["difficulty"],
                      "barriers": r["barriers"], "information_gaps": r["information_gaps"],
                      "tasks": " ".join(t["task_id"] for t in key["tasks"]),
                      "expected_signoffs": r["approval_actions_expected"],
                      "reviewer": "", "decision (accept / change)": "", "change needed": "", "date": ""})
    with open(fr / "review_sheet.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(sheet[0]))
        w.writeheader()
        w.writerows(sheet)
    print(f"independent check: {len(subset)} cases -> {ic}")
    print(f"full review: {len(sheet)} cases -> {fr}")


if __name__ == "__main__":
    main()
