"""Shared result type and command line for the baselines.

Every system (B1, B2, and the pipeline) returns a ``DischargePlan`` so one
scorer can compare them. Baselines write no audit trail; that absence is part
of what the governance comparison (H4) measures.
"""
from __future__ import annotations

import argparse
import importlib
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

from src.models.plan import DischargePlan

input_reader = importlib.import_module("src.pipeline.01_input_reader")


@dataclass
class BaselineResult:
    system: str
    case_id: str
    status: str
    plan: Optional[DischargePlan] = None
    error: Optional[str] = None
    notes: list[str] = field(default_factory=list, metadata={"doc": "Output items dropped while normalizing."})
    raw_output: Optional[str] = None


def load_case(path: str | Path, system: str):
    """Return (case, None) or (None, failed BaselineResult). Same validation as pipeline stage 01."""
    loaded = input_reader.read_case(path)
    if loaded.case is None:
        return None, BaselineResult(system, loaded.case_id, "failed", error=loaded.error)
    return loaded.case, None


def main(system: str, run: Callable[[Path], BaselineResult], argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog=f"python -m baselines.{system}")
    p.add_argument("cases", nargs="+", type=Path, help="case JSON files or directories of them")
    p.add_argument("--out", type=Path, help="write each plan to <out>/<case_id>.json")
    args = p.parse_args(argv)

    paths = [f for c in args.cases for f in (sorted(c.glob("*.json")) if c.is_dir() else [c])]
    failed = 0
    for path in paths:
        r = run(path)
        if r.status != "succeeded":
            failed += 1
            print(f"{r.case_id}: FAILED {r.error}", file=sys.stderr)
            continue
        dropped = f", {len(r.notes)} items dropped" if r.notes else ""
        print(f"{r.case_id}: {len(r.plan.barriers)} barriers, {len(r.plan.information_gaps)} gaps, "
              f"{len(r.plan.tasks)} tasks, {len(r.plan.actions)} actions{dropped}")
        if args.out:
            args.out.mkdir(parents=True, exist_ok=True)
            (args.out / f"{r.case_id}.json").write_text(r.plan.model_dump_json(indent=2))
    return 1 if failed else 0
