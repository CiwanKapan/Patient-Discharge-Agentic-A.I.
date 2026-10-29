"""Score saved runs of B1, B2, B3, and the agentic pipeline against the answer keys.

Reads plans already on disk; it never calls a model, so it costs no API credits.

    python -m evaluation.evaluate --experiment runs/pilot     # a scripts/run_experiment.py run
    python -m evaluation.evaluate --system B1=runs/b1 --system Agentic=runs/agentic
    python -m evaluation.evaluate --experiment runs/main --cases CASE-151 CASE-152

--experiment reads runs/<name>/<arm>/r<k>/ for every arm and run (arms b1, b2, b3,
agentic are reported as B1, B2, B3, Agentic). --system NAME=DIR scores one
directory per system as a single run; audit logs are read from --audit
NAME=DIR, or from DIR/audit when it exists.

Writes to --out (default <experiment>/eval, or runs/eval):
    per_case.csv      one row per system, run, and case
    summary.csv       one row per system and slice (all cases, each difficulty, each
                      condition), pooled over runs, with retry, token, and cost totals
    significance.csv  paired tests of --reference (default Agentic) against each other
                      system for H1-H4 (evaluation/stats.py). H1-H4 against B1 and B2
                      are the primary family. The secondary family, Holm-adjusted on
                      its own, holds H4-strict (compliant in every run) and every
                      comparison with B3 (B2+scaffold).
    variability.csv   for systems with 2+ runs: each metric per run on the cases every
                      run covers, with mean, SD, min, and max across runs

Refuses to score when the LLM arms recorded different settings (model, effort,
max_tokens, max_attempts), and warns when runs came from different commits,
prompts, taxonomy, or dataset files.

Scoring rules:
* The cases scored are those given with --cases, or else every case that has a
  plan or a run record in at least one run. A system with no plan for one of
  those cases is scored as an empty plan, so every system is compared on the
  same cases. Its status is "failed" when its run record or audit log shows a
  failed run (the error is copied into per_case.csv), else "missing".
* Precision and recall are micro-averaged: counts are summed over cases (and
  runs) first. A ratio with nothing to count is left blank instead of 1.0.
* Significance tests use one value per case: the mean over its runs, for every
  hypothesis. For H4 that is the share of the case's runs with no violation;
  the secondary H4-strict counts a case as compliant only if every run was. If runs cover cases
  unevenly (the reduced design: 1 run on all cases, 3 on a subset), the tests
  use run 1 only, so every case counts once; the subset feeds variability.csv.
* H3 plan_completeness (PROVISIONAL): covered / required plan components, where
  each keyed task needs a complete_task recommendation and each keyed
  information gap a verify_information one. See metrics.plan_coverage.
* H4 governance_compliance (PROVISIONAL): share of case runs with zero governance
  violations. Violations are check_governance errors (an approval-required or
  task-gated step not classified for approval, a forbidden tool not classified
  forbidden) plus, for systems with an audit log, audit trail errors. A missing
  or failed plan has no violations to count, so check `failed` next to it.
* Retries and tokens come from each case's run record: format_retries (all LLM
  arms), validation_retries (the pipeline only), and the estimated cost from
  config/run_config.json pricing (batch calls at the batch discount).
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from evaluation import stats  # noqa: E402
from evaluation.metrics import Counts, Score, plan_coverage, score_case  # noqa: E402
from src.models.answer_key import AnswerKey  # noqa: E402
from src.models.audit import check_audit_trail  # noqa: E402
from src.models.case import PatientCase  # noqa: E402
from src.models.messages import BarrierDetection, TaskDetection  # noqa: E402
from src.models.plan import ApprovalDecisions, DischargePlan, RecommendationSet, check_governance  # noqa: E402
from src.utils.audit_logger import read_audit_log  # noqa: E402
from src.utils.run_config import ConfigMismatch, load_run_config, require_same  # noqa: E402
from src.utils.run_records import case_set_of, read_manifest, read_run  # noqa: E402

ARM_NAMES = {"b1": "B1", "b2": "B2", "b3": "B3", "agentic": "Agentic"}
SECONDARY = ("B3",)
CASE_FILE = re.compile(r"^((?:CASE|DEV)-\d{3})(\.run)?\.json$")  # a plan or a run record
TOKEN_FIELDS = ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")


@dataclass
class RunDir:
    run: str
    plans: Path
    audit: Path | None = None
    scope: set[str] | None = None  # the cases this run was asked to cover; None means all

    def covers(self, case_id: str) -> bool:
        return self.scope is None or case_id in self.scope


@dataclass
class Slice:
    score: Score = field(default_factory=Score)
    coverage: Counts = field(default_factory=Counts)
    compliant: int = 0
    failed: int = 0
    violations: int = 0
    llm: dict = field(default_factory=lambda: defaultdict(int))

    def summary(self) -> dict:
        n = self.score.cases
        return {
            **defined(self.score),
            "failed": self.failed,
            "plan_completeness": self.coverage.recall if self.coverage.tp + self.coverage.fn else None,
            "governance_compliance": self.compliant / n if n else None,
            "governance_violations": self.violations,
            **{k: _fmt(v) for k, v in self.llm.items()},
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


def load_plan(rd: RunDir, case_id: str) -> tuple[DischargePlan, str, list[str], str, dict]:
    """(plan, status, audit errors, error message, run record). A missing plan becomes an empty one."""
    record = read_run(rd.plans, case_id)
    audit = Path(record["audit_path"]) if record.get("audit_path") else latest_audit(rd.audit, case_id)
    events = read_audit_log(audit) if audit and audit.exists() else []
    audit_errors = check_audit_trail(events) if events else []
    path = rd.plans / f"{case_id}.json"
    if path.exists():
        return DischargePlan.model_validate_json(path.read_text()), "ok", audit_errors, "", record
    done = next((e.details for e in reversed(events) if e.event_type == "run_completed"), None)
    if record.get("status") == "failed":
        status, error = "failed", record.get("error") or ""
    elif done and done.status == "failed":
        status, error = "failed", done.error or ""
    else:
        status, error = "missing", ""
    return DischargePlan(case_id=case_id, summary=""), status, audit_errors, error, record


def governance_errors(taxonomy: dict, plan: DischargePlan) -> list[str]:
    return check_governance(
        taxonomy,
        RecommendationSet(recommendations=[a.recommendation for a in plan.actions]),
        ApprovalDecisions(classifications=[a.approval for a in plan.actions]),
    )


def llm_usage(record: dict, pricing) -> dict:
    calls = record.get("llm_calls") or []
    out = {
        "llm_calls": len(calls),
        "format_retries": sum(c["outcome"] == "format_error" for c in calls),
        "validation_retries": sum(c["outcome"] == "validation_error" for c in calls),
        "llm_errors": sum(c["outcome"] == "llm_error" for c in calls),
        **{k: sum(c.get(k) or 0 for c in calls) for k in TOKEN_FIELDS},
    }
    out["cost_usd"] = round(pricing.cost(calls), 6) if pricing else None
    return out


def cases_in(rd: RunDir) -> set[str]:
    return {m.group(1) for f in rd.plans.glob("*.json") if (m := CASE_FILE.match(f.name))} \
        if rd.plans.is_dir() else set()


def evaluate(systems: dict[str, list[RunDir]], case_ids: list[str], dataset: Path, keys_dir: Path,
             taxonomy: dict, pricing=None) -> tuple[list[dict], list[dict], list[dict]]:
    rows, slices = [], defaultdict(Slice)
    per_run = defaultdict(Slice)  # (system, run) over the cases every run of the system covers
    common = {name: set(case_ids).intersection(*(rd.scope or case_ids for rd in rds)) if len(rds) > 1 else set()
              for name, rds in systems.items()}
    barrier_sets = defaultdict(list)
    for cid in case_ids:
        cdir, kdir = (dataset, keys_dir) if case_set_of(cid) == "eval" else (ROOT / "data" / "dev" / "cases",
                                                                            ROOT / "data" / "dev" / "answer_keys")
        case = PatientCase.model_validate_json((cdir / f"{cid}.json").read_text())
        key = AnswerKey.model_validate_json((kdir / f"{cid}.key.json").read_text())
        for name, rds in systems.items():
            for rd in rds:
                if not rd.covers(cid):
                    continue
                plan, status, audit_errors, error, record = load_plan(rd, cid)
                one = score_case(key, BarrierDetection(barriers=plan.barriers, information_gaps=plan.information_gaps),
                                 TaskDetection(tasks=plan.tasks), actions=plan.actions, taxonomy=taxonomy)
                covered, required = plan_coverage(key, plan.actions)
                violations = governance_errors(taxonomy, plan) + audit_errors
                usage = llm_usage(record, pricing)
                labels = ["all", f"difficulty={case.difficulty}", f"condition={case.condition}"]
                targets = [slices[(name, label)] for label in labels]
                if cid in common[name]:
                    targets.append(per_run[(name, rd.run)])
                    barrier_sets[(name, cid)].append(frozenset(b.barrier_id for b in plan.barriers))
                for s in targets:
                    score_case(key, BarrierDetection(barriers=plan.barriers, information_gaps=plan.information_gaps),
                               TaskDetection(tasks=plan.tasks), into=s.score, actions=plan.actions, taxonomy=taxonomy)
                    s.coverage.tp += covered
                    s.coverage.fn += required - covered
                    s.compliant += not violations
                    s.failed += status != "ok"
                    s.violations += len(violations)
                    for k, v in usage.items():
                        s.llm[k] += v or 0
                rows.append({
                    "system": name, "run": rd.run, "case_id": cid, "condition": case.condition,
                    "difficulty": case.difficulty, "status": status,
                    **{k: _fmt(v) for k, v in defined(one).items() if k != "cases"},
                    "barriers_flagged": " ".join(sorted(b.barrier_id for b in plan.barriers)),
                    "barriers_missed": " ".join(sorted({b.barrier_id for b in key.barriers}
                                                       - {b.barrier_id for b in plan.barriers})),
                    "barriers_extra": " ".join(sorted({b.barrier_id for b in plan.barriers}
                                                      - {b.barrier_id for b in key.barriers})),
                    "plan_completeness": _fmt(covered / required) if required else None,
                    "unaddressed_barriers": " ".join(plan.unaddressed_barriers),
                    "denied_tool_calls": len(plan.denied_tool_calls),
                    "items_dropped": len(record.get("notes") or []),
                    "governance_violations": len(violations),
                    "violation_details": " | ".join(violations),
                    **usage,
                    "error_kind": record.get("error_kind") or "",
                    "error": error,
                })
    order = list(systems)
    summary = [{"system": name, "slice": label, **{k: _fmt(v) for k, v in s.summary().items()}}
               for (name, label), s in sorted(slices.items(), key=lambda kv: (order.index(kv[0][0]),
                                                                               _slice_order(kv[0][1])))]
    return rows, summary, variability(per_run, barrier_sets, common, order)


VARIABILITY_METRICS = ("barrier_recall", "barrier_precision", "task_recall", "plan_completeness",
                       "approval_recall", "governance_compliance")


def variability(per_run, barrier_sets, common, order) -> list[dict]:
    out = []
    for name in order:
        runs = sorted(r for (n, r) in per_run if n == name)
        if len(runs) < 2:
            continue
        summaries = {r: per_run[(name, r)].summary() for r in runs}
        for metric in VARIABILITY_METRICS:
            values = [summaries[r][metric] for r in runs if summaries[r][metric] is not None]
            if len(values) < 2:
                continue
            out.append({"system": name, "metric": metric, "cases": len(common[name]), "runs": len(values),
                        **{f"value_{r}": _fmt(summaries[r][metric]) for r in runs},
                        "mean": _fmt(statistics.mean(values)), "sd": _fmt(statistics.stdev(values)),
                        "min": _fmt(min(values)), "max": _fmt(max(values))})
        same = [len(set(sets)) == 1 for (n, _), sets in barrier_sets.items() if n == name]
        out.append({"system": name, "metric": "identical_barrier_sets_across_runs", "cases": len(same),
                    "runs": len(runs), "mean": _fmt(sum(same) / len(same)) if same else None})
    return out


def _slice_order(label: str):
    order = {"all": 0, "difficulty=easy": 1, "difficulty=medium": 2, "difficulty=hard": 3}
    return (order.get(label, 4), label)


def _fmt(v):
    return round(v, 4) if isinstance(v, float) else v


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(dict.fromkeys(k for r in rows for k in r)), restval="")
        w.writeheader()
        w.writerows(rows)


# ------------------------------------------------------------------ settings and run discovery
def discover(experiment: Path) -> dict[str, list[RunDir]]:
    systems = {}
    for arm, name in ARM_NAMES.items():
        runs = sorted((d for d in (experiment / arm).glob("r*") if d.is_dir() and d.name[1:].isdigit()),
                      key=lambda d: int(d.name[1:]))
        if runs:
            systems[name] = [RunDir(d.name, d, d / "audit", scope_of(d)) for d in runs]
    return systems


def scope_of(run_dir: Path) -> set[str] | None:
    """The case IDs a run was asked to cover, as recorded in its manifest (None: not recorded, all cases)."""
    cases = read_manifest(run_dir).get("cases")
    return set(cases) if cases else None


def check_settings(systems: dict[str, list[RunDir]]) -> list[str]:
    """Raise ConfigMismatch if LLM arms recorded different settings; return warnings for other differences."""
    settings, identity = {}, defaultdict(set)
    for name, rds in systems.items():
        for rd in rds:
            m = read_manifest(rd.plans)
            recorded = {json.dumps(r["llm_settings"], sort_keys=True)
                        for f in rd.plans.glob("*.run.json") if (r := json.loads(f.read_text())).get("llm_settings")}
            if m.get("llm_settings"):
                recorded.add(json.dumps(m["llm_settings"], sort_keys=True))
            for i, s in enumerate(sorted(recorded)):
                settings[f"{name}/{rd.run}" + (f"#{i}" if i else "")] = json.loads(s)
            for k in ("git_commit", "prompt_version", "taxonomy_sha256", "dataset_manifest_sha256"):
                if m.get(k) is not None and not (k == "prompt_version" and name == "B1"):
                    identity[k].add((m[k], f"{name}/{rd.run}"))
    require_same(settings)
    warnings = []
    for k, seen in identity.items():
        if len({v for v, _ in seen}) > 1:
            groups = defaultdict(list)
            for v, where in seen:
                groups[v].append(where)
            if k == "prompt_version":
                continue  # each arm has its own prompts
            warnings.append(f"runs differ in {k}: " + "; ".join(f"{v[:12]}: {', '.join(sorted(w))}"
                                                               for v, w in groups.items()))
    return warnings


def stats_rows(rows: list[dict], systems: dict[str, list[RunDir]]) -> tuple[list[dict], str]:
    """The rows the significance tests use, and a note on which runs those are."""
    counts = defaultdict(int)
    for r in rows:
        counts[(r["system"], r["case_id"])] += 1
    cases = {r["case_id"] for r in rows}
    uneven = any(len({counts[(name, c)] for c in cases}) > 1 for name in systems)
    if uneven:
        return [r for r in rows if r["run"] == "r1"], "runs cover cases unevenly; tests use run r1 only"
    multi = max(len(rds) for rds in systems.values())
    return rows, (f"tests use each case's mean over its runs (up to {multi})" if multi > 1 else "one run per case")


# ------------------------------------------------------------------ printing
TABLE = [("cases", "case runs"), ("failed", "failed"), ("barrier_recall", "barrier R"),
         ("barrier_precision", "barrier P"), ("cross_field_recall", "xfield R"),
         ("information_gap_recall", "gap R"), ("task_recall", "task R"), ("task_precision", "task P"),
         ("plan_completeness", "complete"), ("approval_recall", "approval R"),
         ("approval_precision", "approval P"), ("approval_label_omissions", "label omit"),
         ("governance_compliance", "gov comply"), ("negative_control_hits", "neg ctl"),
         ("gap_misflags", "gap misflag")]
LLM_TABLE = [("llm_calls", "llm calls"), ("format_retries", "format rtry"), ("validation_retries", "valid rtry"),
             ("llm_errors", "llm errors"), ("input_tokens", "input tok"), ("output_tokens", "output tok"),
             ("cache_read_input_tokens", "cache read"), ("cost_usd", "cost $")]


def print_table(summary: list[dict], label: str, extra=()) -> None:
    rows = [r for r in summary if r["slice"] == label]
    if not rows:
        return
    print(f"\n{label}")
    print(f"{'metric':<12}" + "".join(f"{r['system']:>11}" for r in rows))
    for key, title in [*TABLE, *extra]:
        cells = []
        for r in rows:
            v = r.get(key)
            cells.append(f"{v:>11.2f}" if isinstance(v, float) else f"{'-' if v is None else v:>11}")
        print(f"{title:<12}" + "".join(cells))


def print_significance(rows: list[dict], note: str) -> None:
    print(f"\nsignificance ({rows[0]['reference']} vs each baseline; alternative={rows[0].get('alternative')}; "
          f"Holm-adjusted within each family; {note})")
    print(f"{'':<4}{'metric':<23}{'vs':<9}{'family':<10}{'n':>4}{'nz':>4}{'diff':>8}{'95% CI':>17}{'p':>8}"
          f"{'p_holm':>8}{'effect':>8}")
    for r in rows:
        if r.get("p_value") is None:
            print(f"{r['hypothesis']:<4}{r['metric']:<23}{r['baseline']:<9}{r['family']:<10}{r['n_pairs']:>4}   no pairs")
            continue
        ci = f"[{r['ci95_low']:+.2f}, {r['ci95_high']:+.2f}]"
        flag = "*" if r["significant"] else ""
        small = " (small sample)" if r["small_sample"] else ""
        print(f"{r['hypothesis']:<4}{r['metric']:<23}{r['baseline']:<9}{r['family']:<10}{r['n_pairs']:>4}"
              f"{r['n_nonzero']:>4}{r['mean_difference']:>+8.2f}{ci:>17}{r['p_value']:>8.3f}{r['p_holm']:>8.3f}"
              f"{r['effect_size']:>+8.2f}  {flag}{small}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m evaluation.evaluate", description=__doc__.split("\n")[0])
    p.add_argument("--experiment", type=Path, help="a scripts/run_experiment.py directory, e.g. runs/pilot")
    p.add_argument("--system", action="append", metavar="NAME=PLAN_DIR", help="one system's plan directory; repeatable")
    p.add_argument("--audit", action="append", metavar="NAME=AUDIT_DIR", help="a --system's audit directory")
    p.add_argument("--cases", nargs="+", help="case IDs to score (default: every case with a plan or run record)")
    p.add_argument("--dataset", type=Path, default=ROOT / "data" / "synthetic_cases",
                   help="evaluation cases (DEV-### development cases are always read from data/dev/)")
    p.add_argument("--keys", type=Path, default=ROOT / "data" / "answer_keys")
    p.add_argument("--out", type=Path, help="default <experiment>/eval, or runs/eval")
    p.add_argument("--reference", default="Agentic", help="system the others are tested against")
    p.add_argument("--alternative", default="two-sided", choices=["two-sided", "greater"],
                   help="'greater' tests reference > baseline; choose before looking at results")
    a = p.parse_args(argv)

    if a.experiment:
        systems = discover(a.experiment)
    elif a.system:
        audits = dict(_pair(x) for x in a.audit or [])
        systems = {}
        for name, d in (_pair(x) for x in a.system):
            audit = Path(audits[name]) if name in audits else (Path(d) / "audit" if (Path(d) / "audit").is_dir() else None)
            systems[name] = [RunDir("r1", Path(d), audit)]
    else:
        p.error("pass --experiment DIR or --system NAME=DIR")
    if not systems:
        p.error("no runs found")
    try:
        warnings = check_settings(systems)
    except ConfigMismatch as e:
        print(f"refusing to compare: {e}", file=sys.stderr)
        return 2
    case_ids = a.cases or sorted(set().union(*(cases_in(rd) for rds in systems.values() for rd in rds)))
    if not case_ids:
        p.error("no plans or run records found")
    out = a.out or ((a.experiment / "eval") if a.experiment else Path("runs") / "eval")

    taxonomy = json.loads((ROOT / "config" / "taxonomy.json").read_text())
    pricing = load_run_config().pricing_usd_per_mtok
    rows, summary, var = evaluate(systems, case_ids, a.dataset, a.keys, taxonomy, pricing)
    write_csv(out / "per_case.csv", rows)
    write_csv(out / "summary.csv", summary)
    written = [out / "per_case.csv", out / "summary.csv"]

    for w in warnings:
        print(f"warning: {w}")
    runs = ", ".join(f"{n} x{len(r)}" for n, r in systems.items())
    print(f"Scored {len(case_ids)} cases: {runs} runs.")
    for label in ("all", "difficulty=easy", "difficulty=medium", "difficulty=hard"):
        print_table(summary, label, LLM_TABLE if label == "all" else ())
    if var:
        write_csv(out / "variability.csv", var)
        written.append(out / "variability.csv")
        print("\nrun-to-run variability (see variability.csv):")
        for v in var:
            if v["metric"] in ("barrier_recall", "identical_barrier_sets_across_runs"):
                sd = f", sd {v['sd']:.3f}" if v.get("sd") is not None else ""
                print(f"  {v['system']:<8} {v['metric']:<36} mean {v['mean']}{sd} over {v['cases']} cases")
    others = [n for n in systems if n != a.reference]
    if a.reference in systems and others:
        test_rows, note = stats_rows(rows, systems)
        primary = [n for n in others if n not in SECONDARY]
        secondary = [n for n in others if n in SECONDARY]
        sig = stats.compare(test_rows, a.reference, primary, a.alternative, secondary=secondary)
        write_csv(out / "significance.csv", [{**{k: _fmt(v) for k, v in r.items()}, "runs_used": note} for r in sig])
        print_significance(sig, note)
        written.append(out / "significance.csv")
    print("\nwrote " + ", ".join(map(str, written)))
    return 0


def _pair(s: str) -> tuple[str, str]:
    name, sep, path = s.partition("=")
    if not sep or not name or not path:
        raise SystemExit(f"expected NAME=DIR, got {s!r}")
    return name, path


if __name__ == "__main__":
    sys.exit(main())
