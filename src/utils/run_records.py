"""Per-case output files shared by every arm, plus the run manifest.

For each case an arm writes, into its output directory:

    <case_id>.json          the plan (only when the run succeeded)
    <case_id>.signoff.json  sign-off decisions (arms with a sign-off stage, succeeded runs only)
    <case_id>.run.json      the run record, always: status, error and its kind, items
                            dropped while normalizing, the raw model output (single-prompt
                            arms), every LLM call with its outcome and tokens, the LLM
                            settings, and the audit log path and its check result

A failed run removes any plan or sign-off file an earlier run left, so a stale
plan is never scored. ``manifest.json`` in the same directory records what
produced the run (code version, settings, taxonomy, prompts) so runs made with
different settings are never compared.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[2]


def write_run(out: Path, *, system: str, case_id: str, status: str, plan=None, error: Optional[str] = None,
              error_kind: Optional[str] = None, notes=(), raw_output: Optional[str] = None, llm_calls=(),
              signoffs=None, audit_path=None, audit_errors=(), llm_settings: Optional[dict] = None) -> None:
    out.mkdir(parents=True, exist_ok=True)
    plan_file, signoff_file = out / f"{case_id}.json", out / f"{case_id}.signoff.json"
    if plan is not None:
        plan_file.write_text(plan.model_dump_json(indent=2))
    else:
        plan_file.unlink(missing_ok=True)
    if plan is not None and signoffs is not None:
        signoff_file.write_text(json.dumps({"decisions": [d.model_dump(mode="json") for d in signoffs]}, indent=2) + "\n")
    else:
        signoff_file.unlink(missing_ok=True)
    record = {
        "system": system, "case_id": case_id, "status": status, "error": error, "error_kind": error_kind,
        "notes": list(notes), "raw_output": raw_output,
        "llm_calls": [c.model_dump(mode="json") for c in llm_calls],
        "llm_settings": llm_settings,
        "audit_path": str(audit_path) if audit_path else None, "audit_errors": list(audit_errors),
        "written_at": datetime.now(timezone.utc).isoformat(),
    }
    (out / f"{case_id}.run.json").write_text(json.dumps(record, indent=2) + "\n")


def read_run(out: Path, case_id: str) -> dict:
    path = out / f"{case_id}.run.json"
    return json.loads(path.read_text()) if path.exists() else {}


def is_done(out: Path, case_id: str) -> bool:
    """For resuming: a case is done unless it was never run or failed for infrastructure reasons."""
    r = read_run(out, case_id)
    return bool(r) and not (r["status"] != "succeeded" and r.get("error_kind") in (None, "infrastructure"))


# ------------------------------------------------------------------ manifest
def sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def code_version() -> dict:
    def git(*args):
        try:
            return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
        except (OSError, subprocess.CalledProcessError):
            return None
    status = git("status", "--porcelain", "--untracked-files=no")
    return {"git_commit": git("rev-parse", "HEAD"), "git_dirty": bool(status) if status is not None else None}


def build_manifest(arm: str, llm_settings: Optional[dict], prompt_version: Optional[str], extra: Optional[dict] = None) -> dict:
    taxonomy = ROOT / "config" / "taxonomy.json"
    return {
        "arm": arm,
        **code_version(),
        "llm_settings": llm_settings,
        "prompt_version": prompt_version,
        "taxonomy_version": json.loads(taxonomy.read_text())["meta"]["version"],
        "taxonomy_sha256": sha256(taxonomy),
        "dataset_manifest_sha256": sha256(ROOT / "data" / "dataset_manifest.csv"),
        **(extra or {}),
    }


IDENTITY_KEYS = ("arm", "git_commit", "llm_settings", "prompt_version", "taxonomy_sha256", "dataset_manifest_sha256")


def write_manifest(out: Path, manifest: dict) -> None:
    """Write manifest.json, or refuse if the directory already holds a run made differently."""
    out.mkdir(parents=True, exist_ok=True)
    path = out / "manifest.json"
    if path.exists():
        old = json.loads(path.read_text())
        changed = [k for k in IDENTITY_KEYS if old.get(k) != manifest.get(k)]
        if changed:
            raise RuntimeError(f"{out} holds a run made with different {', '.join(changed)}; "
                               "use a new output directory instead of mixing them")
        cases = sorted(set(old.get("cases") or []) | set(manifest.get("cases") or [])) or None
        manifest = {**old, "cases": cases,
                    "resumed_at": [*old.get("resumed_at", []), datetime.now(timezone.utc).isoformat()]}
    else:
        manifest = {**manifest, "started_at": datetime.now(timezone.utc).isoformat()}
    path.write_text(json.dumps(manifest, indent=2) + "\n")


def read_manifest(out: Path) -> dict:
    path = Path(out) / "manifest.json"
    return json.loads(path.read_text()) if path.exists() else {}
