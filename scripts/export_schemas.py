"""Export JSON Schemas from the Pydantic models in src/models.

The Pydantic models are the source of truth. Run this after changing them:

    python scripts/export_schemas.py

tests/test_contracts.py fails if the committed schema files are out of date.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.models.answer_key import AnswerKey, Scenario  # noqa: E402
from src.models.case import PatientCase  # noqa: E402
from src.models.messages import (  # noqa: E402
    BarrierDetectionMessage,
    CaseSummaryMessage,
    TaskDetectionMessage,
)

SCHEMAS = {
    "data/schemas/patient_case_schema.json": PatientCase,
    "data/schemas/answer_key_schema.json": AnswerKey,
    "data/schemas/scenario_schema.json": Scenario,
    "data/schemas/messages/case_summary_message.json": CaseSummaryMessage,
    "data/schemas/messages/barrier_detection_message.json": BarrierDetectionMessage,
    "data/schemas/messages/task_detection_message.json": TaskDetectionMessage,
}


def render(model) -> str:
    return json.dumps(model.model_json_schema(), indent=2) + "\n"


def main() -> None:
    for rel, model in SCHEMAS.items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render(model))
        print(f"wrote {rel}")


if __name__ == "__main__":
    main()
