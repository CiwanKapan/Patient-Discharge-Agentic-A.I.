"""Run the pipeline on one or more case files.

    python -m src.pipeline data/synthetic_cases/CASE-001.json
    python -m src.pipeline data/synthetic_cases/ --audit-dir runs/audit --out runs/plans

Needs Anthropic credentials (ANTHROPIC_API_KEY, or an `ant auth login` profile).
The model comes from CLAUDE_MODEL, default claude-sonnet-5-5.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.pipeline.runner import DEFAULT_AUDIT_DIR, run_case
from src.utils.llm import AnthropicLLM


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m src.pipeline", description=__doc__.split("\n\n")[0])
    p.add_argument("cases", nargs="+", type=Path, help="case JSON files or directories of them")
    p.add_argument("--audit-dir", type=Path, default=DEFAULT_AUDIT_DIR)
    p.add_argument("--out", type=Path, help="write each plan to <out>/<case_id>.json")
    p.add_argument("--model", help="override CLAUDE_MODEL")
    p.add_argument("--effort", default="medium", choices=["low", "medium", "high", "xhigh", "max"])
    p.add_argument("--max-attempts", type=int, default=2, help="LLM attempts per stage before the run fails")
    args = p.parse_args(argv)

    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    paths = [f for c in args.cases for f in (sorted(c.glob("*.json")) if c.is_dir() else [c])]
    llm = AnthropicLLM(model=args.model, effort=args.effort)
    failed = 0
    for path in paths:
        r = run_case(path, llm, audit_dir=args.audit_dir, max_attempts=args.max_attempts)
        problems = f" audit: {'; '.join(r.audit_errors)}" if r.audit_errors else ""
        if r.status == "succeeded":
            print(f"{r.case_id}: {len(r.plan.barriers)} barriers, {len(r.plan.tasks)} tasks, "
                  f"{len(r.plan.actions)} actions, {len(r.plan.denied_tool_calls)} denied calls{problems}")
            if args.out:
                args.out.mkdir(parents=True, exist_ok=True)
                (args.out / f"{r.case_id}.json").write_text(r.plan.model_dump_json(indent=2))
        else:
            failed += 1
            print(f"{r.case_id}: FAILED {r.error}{problems}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
