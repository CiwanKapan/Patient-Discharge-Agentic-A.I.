"""Stage 01 - Input Reader (deterministic).

Reads a raw case file, hashes it for the audit log (AU-01), and validates it
against ``PatientCase``. Malformed input fails loudly: the run stops here and
no later stage sees a partially valid case.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from pydantic import ValidationError

from src.models.audit import CaseLoadedDetails
from src.models.case import PatientCase
from src.models.messages import Stage

STAGE = Stage.INPUT_READER


@dataclass
class LoadedCase:
    case_id: str
    details: CaseLoadedDetails
    case: Optional[PatientCase] = None
    error: Optional[str] = None


def read_case(path: str | Path) -> LoadedCase:
    """Load and validate one case file.

    Never raises for bad content. A file that cannot be validated comes back
    with ``case=None`` and an ``error``, so the runner can still log AU-01 with
    ``schema_valid=False`` before failing the run. ``case_id`` falls back to the
    file name when the file has no readable one.
    """
    path = Path(path)
    raw = path.read_bytes()
    details = dict(source=str(path), case_sha256=hashlib.sha256(raw).hexdigest())
    try:
        case = PatientCase.model_validate_json(raw)
    except ValidationError as e:
        try:
            case_id = str(json.loads(raw).get("case_id") or path.stem)
        except (ValueError, AttributeError):
            case_id = path.stem
        problems = "; ".join(f"{'.'.join(map(str, err['loc']))}: {err['msg']}" for err in e.errors()[:10])
        return LoadedCase(case_id, CaseLoadedDetails(**details, schema_valid=False), error=f"invalid case: {problems}")
    return LoadedCase(case.case_id, CaseLoadedDetails(**details, schema_valid=True), case=case)
