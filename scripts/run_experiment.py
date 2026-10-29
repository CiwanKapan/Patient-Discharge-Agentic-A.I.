"""Run the arms of the benchmark into one experiment directory.

    python scripts/run_experiment.py --name pilot --case-set dev --runs 1-3   # 15 development cases
    python scripts/run_experiment.py --name main --runs 1-3                  # full design: 3 runs, all cases
    python scripts/run_experiment.py --name main --runs 1                    # reduced design, step 1
    python scripts/run_experiment.py --name main --runs 2-3 --cases-file data/subsets/stratified_40.txt
    python scripts/run_experiment.py --name pilot ... --dry-run              # print the plan, call nothing

--case-set eval (default) runs the 160 evaluation cases; --case-set dev runs the
15 development cases in data/dev/ (DEV-###), which are for pilots and checks and
never part of the results. One experiment uses one case set.

Layout: runs/<name>/<arm>/r<k>/ holds each arm's plans, run records, audit logs
(audit/), and manifest.json. B1 is deterministic and runs once (r1 only).

Every LLM arm (B2, agentic) is built from the same settings in
config/run_config.json. The run refuses to start if:
  * CLAUDE_MODEL overrides the configured model,
  * the working tree has uncommitted changes (results must tie to a commit;
    --allow-dirty overrides this for trial runs), or
  * a run directory already holds a run made with a different commit,
    settings, prompts, taxonomy, or dataset.
Re-running the same command resumes: finished cases are skipped, and cases that
failed for infrastructure reasons (rate limits, server or connection errors)
are run again. B2 goes through the Batch API unless --no-batch.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from baselines import baseline_1_rule_based as b1  # noqa: E402
from baselines import baseline_2_single_llm as b2  # noqa: E402
from baselines._common import save as save_baseline  # noqa: E402
from src.pipeline import __main__ as pipeline_cli  # noqa: E402
from src.pipeline._common import PROMPT_VERSION, load_taxonomy  # noqa: E402
from src.pipeline.runner import run_case as run_pipeline  # noqa: E402
from src.utils.run_config import check_environment, load_run_config  # noqa: E402
from src.utils.run_records import CASE_SETS, build_manifest, case_files, case_path, case_set_of, code_version, is_done, write_manifest  # noqa: E402

ARMS = ("b1", "b2", "agentic")
LLM_ARMS = ("b2", "agentic")
PROMPTS = {"b1": None, "b2": b2.PROMPT_VERSION, "agentic": PROMPT_VERSION}
# Model calls per case for one attempt; a format or validation retry adds calls.
CALLS_PER_CASE = {"b1": 0, "b2": 1, "agentic": 4}


def parse_runs(text: str) -> list[int]:
    lo, _, hi = text.partition("-")
    runs = list(range(int(lo), int(hi or lo) + 1))
    if not runs or runs[0] < 1:
        raise argparse.ArgumentTypeError(f"bad --runs {text!r}; use e.g. 1 or 1-3")
    return runs


def read_cases(cases_file: Path | None, case_set: str = "eval") -> list[Path]:
    if cases_file is None:
        return case_files(CASE_SETS[case_set][0])
    ids = [line.strip() for line in cases_file.read_text().splitlines() if line.strip() and not line.startswith("#")]
    wrong = sorted(i for i in ids if case_set_of(i) != case_set)
    if wrong:
        raise SystemExit(f"--cases-file lists cases outside --case-set {case_set}: {', '.join(wrong[:5])}")
    return [case_path(cid) for cid in ids]


def plan(arms, runs, paths, root):
    """(arm, run, out_dir, paths still to do) for every arm and run, and the most model calls they could make."""
    jobs, max_calls = [], 0
    for k in runs:
        for arm in arms:
            if arm == "b1" and k > 1:
                continue
            out = root / arm / f"r{k}"
            todo = [p for p in paths if not is_done(out, p.stem)]
            jobs.append((arm, k, out, todo))
            max_calls += len(todo) * CALLS_PER_CASE[arm]
    return jobs, max_calls


def main(argv=None, llm=None) -> int:
    """``llm`` replaces the Anthropic client (tests pass an offline stand-in)."""
    p = argparse.ArgumentParser(prog="python scripts/run_experiment.py", description=__doc__.split("\n\n")[0])
    p.add_argument("--name", required=True, help="experiment name; results go to runs/<name>/")
    p.add_argument("--runs", type=parse_runs, default=[1], help="run numbers, e.g. 1 or 1-3 (default 1)")
    p.add_argument("--arms", default=",".join(ARMS), help=f"comma-separated subset of {','.join(ARMS)}")
    p.add_argument("--case-set", default="eval", choices=sorted(CASE_SETS),
                   help="eval: the 160 evaluation cases (default); dev: the 15 development cases")
    p.add_argument("--cases-file", type=Path, help="one case ID per line (default: every case in the case set)")
    p.add_argument("--runs-dir", type=Path, default=ROOT / "runs")
    p.add_argument("--no-batch", action="store_true", help="call B2 one case at a time instead")
    p.add_argument("--allow-dirty", action="store_true", help="allow uncommitted changes (trial runs only)")
    p.add_argument("--dry-run", action="store_true", help="print what would run; call nothing, write nothing")
    a = p.parse_args(argv)

    arms = [x.strip() for x in a.arms.split(",") if x.strip()]
    if unknown := set(arms) - set(ARMS):
        p.error(f"unknown arms: {sorted(unknown)}")
    cfg = load_run_config()
    settings = cfg.llm
    check_environment(settings)
    version = code_version()
    if version["git_dirty"] and not a.allow_dirty and not a.dry_run:
        p.error("uncommitted changes: commit first so results tie to a commit, or pass --allow-dirty for a trial run")
    paths = read_cases(a.cases_file, a.case_set)
    root = a.runs_dir / a.name
    jobs, max_calls = plan(arms, a.runs, paths, root)
    batch = cfg.batch_single_prompt_arms and not a.no_batch

    print(f"experiment {root} | commit {version['git_commit']}{' (dirty)' if version['git_dirty'] else ''}")
    print(f"case set: {a.case_set} ({len(paths)} cases)")
    print(f"settings: {settings.model_dump()} | B2 via {'Batch API' if batch else 'direct calls'}")
    for arm, k, out, todo in jobs:
        print(f"  {arm:8} r{k}: {len(todo)} of {len(paths)} cases to run")
    print(f"model calls: at least {max_calls} (more if responses are retried; "
          f"up to {settings.max_attempts}x per call)")
    if a.dry_run:
        return 0

    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    taxonomy = load_taxonomy()
    s = settings.model_dump()
    if llm is None and any(arm in LLM_ARMS and todo for arm, _, _, todo in jobs):
        from src.utils.llm import AnthropicLLM
        llm = AnthropicLLM.from_settings(settings)
    extra = {"experiment": a.name, "cases_file": str(a.cases_file) if a.cases_file else None, "batch": batch}

    # Stamp every run directory up front, so the commit and file hashes describe the
    # state the whole experiment started from, even if files change while it runs.
    manifests = {(arm, k): build_manifest(arm, s if arm in LLM_ARMS else None, PROMPTS[arm],
                                          {**extra, "run": k, "cases": [x.stem for x in paths]}, case_set=a.case_set)
                 for arm, k, _, _ in jobs}
    failed = 0
    for arm, k, out, todo in jobs:
        write_manifest(out, manifests[(arm, k)])
        if not todo:
            continue
        print(f"\n== {arm} r{k}: {len(todo)} cases")
        if arm == "agentic":
            for path in todo:
                r = run_pipeline(path, llm, taxonomy=taxonomy, audit_dir=out / "audit",
                                 max_attempts=settings.max_attempts, llm_settings=s)
                pipeline_cli.save(out, r, s)
                failed += not pipeline_cli.report(r)
            continue
        if arm == "b1":
            results = (b1.run_case(path, taxonomy) for path in todo)
        else:
            kw = dict(taxonomy=taxonomy, max_attempts=settings.max_attempts)
            results = (b2.run_cases_batch(todo, llm, **kw, on_poll=_progress(arm, k)) if batch
                       else (b2.run_case(path, llm, **kw) for path in todo))
        for r in results:
            if arm in LLM_ARMS:
                r.llm_settings = s
            save_baseline(out, r)
            failed += r.status != "succeeded"
            if r.status != "succeeded":
                print(f"{r.case_id}: FAILED {r.error}", file=sys.stderr)
    print(f"\ndone; {failed} failed case runs. Score with: python -m evaluation.evaluate --experiment {root}")
    return 1 if failed else 0


def _progress(arm, k):
    def show(batch):
        c = batch.request_counts
        print(f"  {arm} r{k} batch {batch.id}: {batch.processing_status} "
              f"({c.succeeded} done, {c.processing} processing, {c.errored} errored)", flush=True)
    return show


if __name__ == "__main__":
    sys.exit(main())
