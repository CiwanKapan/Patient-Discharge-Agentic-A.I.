"""Run the pipeline on one or more case files.

    python -m src.pipeline data/synthetic_cases/CASE-001.json
    python -m src.pipeline data/synthetic_cases/ --out runs/agentic

Needs Anthropic credentials (ANTHROPIC_API_KEY, or an `ant auth login` profile).
Model, effort, max_tokens, and attempts per stage come from config/run_config.json,
the same settings B2 and B3 use; the run refuses to start if CLAUDE_MODEL disagrees.

With --out, each case gets a plan, a sign-off file, and a run record (see
src/utils/run_records.py), and the directory gets manifest.json. Audit logs go
to --audit-dir (default <out>/audit, or runs/audit without --out).
--skip-existing resumes: finished cases are skipped; cases that failed for
infrastructure reasons are run again.

--signoff picks the stage 09 reviewer: pending (default; no clinician, every gated
action stays pending) or approve_all (a simulated clinician approves them all).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.pipeline._common import PROMPT_VERSION
from src.pipeline.runner import DEFAULT_AUDIT_DIR, RunResult, run_case, signoff
from src.utils.llm import AnthropicLLM
from src.utils.run_config import check_environment, load_run_config
from src.utils.run_records import build_manifest, is_done, write_manifest, write_run

SYSTEM = "agentic"


def save(out: Path, r: RunResult, llm_settings: dict) -> None:
    write_run(out, system=SYSTEM, case_id=r.case_id, status=r.status, plan=r.plan, error=r.error,
              error_kind=r.error_kind, llm_calls=r.llm_calls, signoffs=r.signoffs if r.plan else None,
              audit_path=r.audit_path, audit_errors=r.audit_errors, llm_settings=llm_settings)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m src.pipeline", description=__doc__.split("\n\n")[0])
    p.add_argument("cases", nargs="+", type=Path, help="case JSON files or directories of them")
    p.add_argument("--out", type=Path, help="write plans, run records, and manifest.json here")
    p.add_argument("--audit-dir", type=Path, help="audit logs (default: <out>/audit, or runs/audit)")
    p.add_argument("--skip-existing", action="store_true", help="resume: skip cases already finished in --out")
    p.add_argument("--signoff", default="pending", choices=sorted(signoff.REVIEWERS),
                   help="reviewer for stage 09 sign-off (default: pending, no clinician)")
    args = p.parse_args(argv)

    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    settings = load_run_config().llm
    check_environment(settings)
    s = settings.model_dump()
    paths = [f for c in args.cases for f in (sorted(c.glob("CASE-*.json")) if c.is_dir() else [c])]
    audit_dir = args.audit_dir or (args.out / "audit" if args.out else DEFAULT_AUDIT_DIR)
    if args.out:
        write_manifest(args.out, build_manifest(SYSTEM, s, PROMPT_VERSION))
        if args.skip_existing:
            paths = [x for x in paths if not is_done(args.out, x.stem)]
    llm = AnthropicLLM.from_settings(settings)
    reviewer = signoff.REVIEWERS[args.signoff]()
    failed = 0
    for path in paths:
        r = run_case(path, llm, audit_dir=audit_dir, max_attempts=settings.max_attempts, reviewer=reviewer,
                     llm_settings=s)
        if args.out:
            save(args.out, r, s)
        failed += not report(r)
    return 1 if failed else 0


def report(r: RunResult) -> bool:
    problems = f" audit: {'; '.join(r.audit_errors)}" if r.audit_errors else ""
    if r.status != "succeeded":
        print(f"{r.case_id}: FAILED {r.error}{problems}", file=sys.stderr)
        return False
    counts = {d: sum(s.decision == d for s in r.signoffs) for d in ("approved", "rejected", "pending")}
    signed = ", ".join(f"{n} {d}" for d, n in counts.items() if n) or "none needed"
    retries = {k: sum(c.outcome == k for c in r.llm_calls) for k in ("format_error", "validation_error")}
    print(f"{r.case_id}: {len(r.plan.barriers)} barriers, {len(r.plan.tasks)} tasks, "
          f"{len(r.plan.actions)} actions, {len(r.plan.denied_tool_calls)} denied calls, "
          f"sign-off: {signed}, retries: {retries['format_error']} format / {retries['validation_error']} validation"
          f"{problems}")
    return True


if __name__ == "__main__":
    sys.exit(main())
