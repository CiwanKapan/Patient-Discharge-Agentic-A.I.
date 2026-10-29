"""Score saved runs of B1, B2, and the agentic pipeline against the answer keys.

Reads plans already on disk; it never calls a model, so it costs no API credits.
Produce the plans first:

    python -m baselines.baseline_1_rule_based data/synthetic_cases/ --out runs/b1
    python -m baselines.baseline_2_single_llm data/synthetic_cases/ --out runs/b2
    python -m src.pipeline data/synthetic_cases/ --audit-dir runs/audit --out runs/plans

Then, from the repo root:

    python -m evaluation.evaluate                        # every case with a plan from any system
    python -m evaluation.evaluate --cases CASE-151 CASE-152
    python -m evaluation.evaluate --system Agentic=runs/plans_v2 --out runs/eval_v2

Writes <out>/per_case.csv (one row per system and case) and <out>/summary.csv
(one row per system and slice: all cases, each difficulty, each condition), and
prints the overall and per-difficulty tables.

Scoring rules:
* The cases scored are those given with --cases, or else every case that has a
  plan from at least one system. A system with no plan for one of those cases
  is scored as if it returned an empty plan (status "failed" when its audit log
  shows a failed run, else "missing"), so every system is compared on the same
  cases.
* Precision and recall are micro-averaged: counts are summed over cases first.
  A ratio with nothing to count (e.g. cross-field recall on cases without a
  cross-field barrier) is left blank instead of reported as 1.0.
* H3 plan_completeness (PROVISIONAL): covered / required plan components, where
  each keyed task needs a complete_task recommendation and each keyed
  information gap a verify_information one. See metrics.plan_coverage.
* H4 governance_compliance (PROVISIONAL): share of cases with zero governance
  violations. Violations are check_governance errors (an approval-required or
  task-gated step not classified for approval, a forbidden tool not classified
  forbidden) plus, for systems with an audit log, audit trail errors. A missing
  or failed plan has no violations to count, so check `failed` next to it.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from evaluation.metrics import Counts, Score, plan_coverage, score_case  # noqa: E402
from src.models.answer_key import AnswerKey  # noqa: E402
from src.models.audit import check_audit_trail  # noqa: E402
from src.models.case import PatientCase  # noqa: E402
from src.models.messages import BarrierDetection, TaskDetection  # noqa: E402
from src.models.plan import ApprovalDecisions, DischargePlan, RecommendationSet, check_governance  # noqa: E402
from src.utils.audit_logger import read_audit_log  # noqa: E402

DEFAULT_SYSTEMS = {"B1": "runs/b1", "B2": "runs/b2", "Agentic": "runs/plans"}
DEFAULT_AUDIT = {"Agentic": "runs/audit"}


@dataclass
class Slice:
    score: Score = field(default_factory=Score)
    coverage: Counts = field(default_factory=Counts)
    compliant: int = 0
    failed: int = 0
    violations: int = 0

    def summary(self) -> dict:
        n = self.score.cases
        return {
            **defined(self.score),
            "failed": self.failed,
            "plan_completeness": self.coverage.recall if self.coverage.tp + self.coverage.fn else None,
            "governance_compliance": self.compliant / n if n else 1.0,
            "governance_violations": self.violations,
        }


def defined(score: Score) -> dict:
    """Score.summary() with ratios that have nothing to count set to None."""
    out = score.summary()
    for name, c in (("barrier", score.barriers), ("cross_field", score.cross_field),
                    ("information_gap", score.information_gaps), ("task", score.tasks),
                    ("approval", score.approvals)):
        if f"{name}_recall" in out and not c.tp + c.fn:
            out[f"{name}_recall"] = None
        if f"{name}_precision" in out and not c.tp + c.fp:
            out[f"{name}_precision"] = None
    return out


def latest_audit(audit_dir: Path | None, case_id: str) -> Path | None:
    if audit_dir is None or not (audit_dir / case_id).is_dir():
        return None
    logs = sorted((audit_dir / case_id).glob("*.jsonl"), key=lambda p: p.stat().st_mtime)
    return logs[-1] if logs else None


def load_plan(plan_dir: Path, audit_dir: Path | None, case_id: str) -> tuple[DischargePlan, str, list[str], str]:
    """(plan, status, audit errors, error message). A missing plan becomes an empty one."""
    audit = latest_audit(audit_dir, case_id)
    events = read_audit_log(audit) if audit else []
    audit_errors = check_audit_trail(events) if events else []
    path = plan_dir / f"{case_id}.json"
    if path.exists():
        return DischargePlan.model_validate_json(path.read_text()), "ok", audit_errors, ""
    done = next((e.details for e in reversed(events) if e.event_type == "run_completed"), None)
    status, error = ("failed", done.error or "") if done and done.status == "failed" else ("missing", "")
    return DischargePlan(case_id=case_id, summary=""), status, audit_errors, error


def governance_errors(taxonomy: dict, plan: DischargePlan) -> list[str]:
    return check_governance(
        taxonomy,
        RecommendationSet(recommendations=[a.recommendation for a in plan.actions]),
        ApprovalDecisions(classifications=[a.approval for a in plan.actions]),
    )


def evaluate(systems: dict[str, Path], audits: dict[str, Path], case_ids: list[str], dataset: Path,
             keys_dir: Path, taxonomy: dict) -> tuple[list[dict], list[dict]]:
    rows, slices = [], defaultdict(Slice)
    for cid in case_ids:
        case = PatientCase.model_validate_json((dataset / f"{cid}.json").read_text())
        key = AnswerKey.model_validate_json((keys_dir / f"{cid}.key.json").read_text())
        for name, plan_dir in systems.items():
            plan, status, audit_errors, error = load_plan(plan_dir, audits.get(name), cid)
            one = score_case(key, BarrierDetection(barriers=plan.barriers, information_gaps=plan.information_gaps),
                             TaskDetection(tasks=plan.tasks), actions=plan.actions, taxonomy=taxonomy)
            covered, required = plan_coverage(key, plan.actions)
            violations = governance_errors(taxonomy, plan) + audit_errors
            for label in ("all", f"difficulty={case.difficulty}", f"condition={case.condition}"):
                s = slices[(name, label)]
                score_case(key, BarrierDetection(barriers=plan.barriers, information_gaps=plan.information_gaps),
                           TaskDetection(tasks=plan.tasks), into=s.score, actions=plan.actions, taxonomy=taxonomy)
                s.coverage.tp += covered
                s.coverage.fn += required - covered
                s.compliant += not violations
                s.failed += status != "ok"
                s.violations += len(violations)
            rows.append({
                "system": name, "case_id": cid, "condition": case.condition, "difficulty": case.difficulty,
                "status": status,
                **{k: _fmt(v) for k, v in defined(one).items() if k != "cases"},
                "barriers_missed": " ".join(sorted({b.barrier_id for b in key.barriers}
                                                   - {b.barrier_id for b in plan.barriers})),
                "barriers_extra": " ".join(sorted({b.barrier_id for b in plan.barriers}
                                                  - {b.barrier_id for b in key.barriers})),
                "plan_completeness": _fmt(covered / required) if required else None,
                "unaddressed_barriers": " ".join(plan.unaddressed_barriers),
                "denied_tool_calls": len(plan.denied_tool_calls),
                "governance_violations": len(violations),
                "violation_details": " | ".join(violations),
                "error": error,
            })
    summary = [{"system": name, "slice": label, **{k: _fmt(v) for k, v in s.summary().items()}}
               for (name, label), s in sorted(slices.items(), key=lambda kv: (list(systems).index(kv[0][0]),
                                                                               _slice_order(kv[0][1])))]
    return rows, summary


def _slice_order(label: str):
    order = {"all": 0, "difficulty=easy": 1, "difficulty=medium": 2, "difficulty=hard": 3}
    return (order.get(label, 4), label)


def _fmt(v):
    return round(v, 4) if isinstance(v, float) else v


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


TABLE = [("cases", "cases"), ("failed", "failed"), ("barrier_recall", "barrier R"),
         ("barrier_precision", "barrier P"), ("cross_field_recall", "xfield R"),
         ("information_gap_recall", "gap R"), ("task_recall", "task R"), ("task_precision", "task P"),
         ("plan_completeness", "complete"), ("approval_recall", "approval R"),
         ("approval_precision", "approval P"), ("approval_label_omissions", "label omit"),
         ("governance_compliance", "gov comply"), ("negative_control_hits", "neg ctl"),
         ("gap_misflags", "gap misflag")]


def print_table(summary: list[dict], label: str) -> None:
    rows = [r for r in summary if r["slice"] == label]
    if not rows:
        return
    print(f"\n{label}")
    print(f"{'metric':<12}" + "".join(f"{r['system']:>10}" for r in rows))
    for key, title in TABLE:
        print(f"{title:<12}" + "".join(f"{r[key]:>10.2f}" if isinstance(r[key], float)
                                       else f"{'-' if r[key] is None else r[key]:>10}" for r in rows))


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m evaluation.evaluate", description=__doc__.split("\n")[0])
    p.add_argument("--system", action="append", metavar="NAME=PLAN_DIR",
                   help=f"a system's plan directory; repeatable (default: {DEFAULT_SYSTEMS})")
    p.add_argument("--audit", action="append", metavar="NAME=AUDIT_DIR",
                   help=f"a system's audit directory; repeatable (default: {DEFAULT_AUDIT})")
    p.add_argument("--cases", nargs="+", help="case IDs to score (default: every case with a plan)")
    p.add_argument("--dataset", type=Path, default=ROOT / "data" / "synthetic_cases")
    p.add_argument("--keys", type=Path, default=ROOT / "data" / "answer_keys")
    p.add_argument("--out", type=Path, default=Path("runs") / "eval")
    a = p.parse_args(argv)

    systems = {n: Path(d) for n, d in (_pair(x) for x in a.system)} if a.system else \
        {n: Path(d) for n, d in DEFAULT_SYSTEMS.items() if Path(d).is_dir()}
    audits = {n: Path(d) for n, d in (_pair(x) for x in a.audit)} if a.audit else \
        {n: Path(d) for n, d in DEFAULT_AUDIT.items() if n in systems and Path(d).is_dir()}
    if not systems:
        p.error("no plan directories found; run the systems first or pass --system NAME=DIR")
    case_ids = a.cases or sorted({f.stem for d in systems.values() if d.is_dir() for f in d.glob("CASE-*.json")})
    if not case_ids:
        p.error("no plans found in " + ", ".join(map(str, systems.values())))

    taxonomy = json.loads((ROOT / "config" / "taxonomy.json").read_text())
    rows, summary = evaluate(systems, audits, case_ids, a.dataset, a.keys, taxonomy)
    write_csv(a.out / "per_case.csv", rows)
    write_csv(a.out / "summary.csv", summary)

    print(f"Scored {len(case_ids)} cases for {', '.join(systems)}.")
    for label in ("all", "difficulty=easy", "difficulty=medium", "difficulty=hard"):
        print_table(summary, label)
    print(f"\nwrote {a.out / 'per_case.csv'} and {a.out / 'summary.csv'}")
    return 0


def _pair(s: str) -> tuple[str, str]:
    name, sep, path = s.partition("=")
    if not sep or not name or not path:
        raise SystemExit(f"expected NAME=DIR, got {s!r}")
    return name, path


if __name__ == "__main__":
    sys.exit(main())
