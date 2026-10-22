"""Append-only JSONL audit logger (AU-01..AU-08).

One file per run. The logger refuses to open a file that already exists, only
ever appends, assigns sequence numbers itself, and validates every event
against ``src/models/audit.py`` before writing it. Each line is flushed and
fsynced, so a crash mid-run leaves every event written so far on disk.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from src.models.audit import AuditLogLine, _EventBase
from src.models.messages import Stage


class AuditLogger:
    def __init__(self, path: str | Path, run_id: str, case_id: str):
        self.path = Path(path)
        self.run_id = run_id
        self.case_id = case_id
        self._sequence = 0
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = open(self.path, "x", encoding="utf-8")  # "x": never reuse or overwrite a log

    def log(
        self,
        event_cls: type[_EventBase],
        details: BaseModel,
        stage: Optional[Stage] = None,
        message_id: Optional[str] = None,
    ) -> _EventBase:
        event = event_cls(
            run_id=self.run_id,
            case_id=self.case_id,
            sequence=self._sequence,
            stage=stage,
            message_id=message_id,
            details=details,
        )
        self._fh.write(event.model_dump_json() + "\n")
        self._fh.flush()
        os.fsync(self._fh.fileno())
        self._sequence += 1
        return event

    def close(self) -> None:
        self._fh.close()

    def __enter__(self) -> "AuditLogger":
        return self

    def __exit__(self, *exc) -> None:
        self.close()


def read_audit_log(path: str | Path) -> list:
    """Load a JSONL audit log back into typed events (for ``check_audit_trail``)."""
    with open(path, encoding="utf-8") as fh:
        return [AuditLogLine.model_validate_json(line).root for line in fh if line.strip()]
