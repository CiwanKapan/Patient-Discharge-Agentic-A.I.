"""Shared result type and command line for the baselines.

Every system (B1, B2, B3, and the pipeline) returns a ``DischargePlan`` so one
scorer can compare them. B1 and B2 write no audit trail; that absence is part of
what the governance comparison (H4) measures. B3 runs the pipeline's governance
code and writes one.

With ``--out``, each case gets a plan and a run record (see
src/utils/run_records.py), and the directory gets a manifest.json that records
the code version and settings. ``--skip-existing`` resumes an interrupted run:
cases already finished are skipped; cases that failed for infrastructure
reasons (rate limit, server or connection error) are run again.
"""
from __future__ import annotations

import argparse
import importlib
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

from src.models.plan import DischargePlan
from src.utils.run_records import build_manifest, is_done, write_manifest, write_run

input_reader = importlib.import_module("src.pipeline.01_input_reader")


@dataclass
class BaselineResult:
    system: str
    case_id: str
    status: str
    plan: Optional[DischargePlan] = None
    error: Optional[str] = None
    error_kind: Optional[str] = None  # "infrastructure" (a rerun may succeed) or "output" (a result)
    notes: list[str] = field(default_factory=list, metadata={"doc": "Output items dropped while normalizing."})
    raw_output: Optional[str] = None
    llm_calls: list = field(default_factory=list)  # LLMCallRecord per model call
    signoffs: Optional[list] = None  # SignoffDecision per gated action (B3 only)
    audit_path: Optional[Path] = None
    audit_errors: list[str] = field(default_factory=list)
    llm_settings: Optional[dict] = None


def load_case(path: str | Path, system: str):
    """Return (case, None) or (None, failed BaselineResult). Same validation as pipeline stage 01."""
    loaded = input_reader.read_case(path)
    if loaded.case is None:
        return None, BaselineResult(system, loaded.case_id, "failed", error=loaded.error, error_kind="output")
    return loaded.case, None


def save(out: Path, r: BaselineResult) -> None:
    write_run(out, system=r.system, case_id=r.case_id, status=r.status, plan=r.plan, error=r.error,
              error_kind=r.error_kind, notes=r.notes, raw_output=r.raw_output, llm_calls=r.llm_calls,
              signoffs=r.signoffs, audit_path=r.audit_path, audit_errors=r.audit_errors, llm_settings=r.llm_settings)


def report(r: BaselineResult) -> bool:
    if r.status != "succeeded":
        print(f"{r.case_id}: FAILED {r.error}", file=sys.stderr)
        return False
    dropped = f", {len(r.notes)} items dropped" if r.notes else ""
    retries = sum(c.outcome == "format_error" for c in r.llm_calls)
    retried = f", {retries} format retries" if retries else ""
    audit = f", audit: {'; '.join(r.audit_errors)}" if r.audit_errors else ""
    print(f"{r.case_id}: {len(r.plan.barriers)} barriers, {len(r.plan.information_gaps)} gaps, "
          f"{len(r.plan.tasks)} tasks, {len(r.plan.actions)} actions{dropped}{retried}{audit}")
    return True


def case_paths(cases: list[Path]) -> list[Path]:
    return [f for c in cases for f in (sorted(c.glob("CASE-*.json")) if c.is_dir() else [c])]


def main(system: str, run: Optional[Callable[[Path], BaselineResult]], argv: list[str] | None = None, *,
         batch=None, llm_settings: Optional[dict] = None, prompt_version: Optional[str] = None,
         add_args: Optional[Callable] = None, bind: Optional[Callable] = None) -> int:
    """``batch`` is a callable over all paths (or True when ``bind`` supplies it). ``add_args``
    adds arm-specific options; ``bind(args)`` returns (run, batch) built from them."""
    p = argparse.ArgumentParser(prog=f"python -m baselines.{system}")
    p.add_argument("cases", nargs="+", type=Path, help="case JSON files or directories of them")
    p.add_argument("--out", type=Path, help="write plans, run records, and manifest.json here")
    p.add_argument("--skip-existing", action="store_true", help="resume: skip cases already finished in --out")
    if batch is not None:
        p.add_argument("--batch", action="store_true", help="send all cases through the Batch API (50%% price)")
    if add_args:
        add_args(p)
    args = p.parse_args(argv)
    if bind:
        run, batch = bind(args)

    paths = case_paths(args.cases)
    if args.out:
        write_manifest(args.out, build_manifest(system, llm_settings, prompt_version))
        if args.skip_existing:
            paths = [x for x in paths if not is_done(args.out, x.stem)]
    results = batch(paths) if getattr(args, "batch", False) else (run(x) for x in paths)
    failed = 0
    for r in results:
        if args.out:
            save(args.out, r)
        failed += not report(r)
    return 1 if failed else 0
