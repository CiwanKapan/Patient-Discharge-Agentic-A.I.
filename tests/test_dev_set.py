"""The development set in data/dev/: 15 cases for pilots and live checks, kept apart from the 160 evaluation cases."""
import csv
import json
from collections import Counter

from scripts.export_schemas import ROOT
from scripts.generate_cases import validate
from src.models.answer_key import AnswerKey
from src.models.case import PatientCase
from src.utils.run_records import CASE_SETS, case_files

DEV_CASES, DEV_KEYS, DEV_MANIFEST = CASE_SETS["dev"]
EVAL_CASES, _, EVAL_MANIFEST = CASE_SETS["eval"]


def test_one_case_per_condition_and_difficulty():
    cases = [PatientCase.model_validate_json(p.read_text()) for p in case_files(DEV_CASES)]
    assert [c.case_id for c in cases] == [f"DEV-{i:03d}" for i in range(1, 16)]
    assert Counter((c.condition, c.difficulty) for c in cases) == Counter(
        {(cond, d): 1 for cond in ("HF", "CO", "PN", "OR", "ST") for d in ("easy", "medium", "hard")})


def test_every_dev_case_and_key_meets_the_dataset_rules(taxonomy):
    for p in case_files(DEV_CASES):
        case = json.loads(p.read_text())
        key = json.loads((DEV_KEYS / f"{p.stem}.key.json").read_text())
        AnswerKey.model_validate(key)
        assert validate(case, key, taxonomy) == [], p.stem


def test_dev_set_is_separate_from_the_evaluation_set():
    assert not any(p.stem.startswith("DEV-") for p in EVAL_CASES.glob("*.json"))
    assert not any(r["case_id"].startswith("DEV-") for r in csv.DictReader(EVAL_MANIFEST.open()))
    assert {r["case_id"] for r in csv.DictReader(DEV_MANIFEST.open())} == {p.stem for p in case_files(DEV_CASES)}
    strip = lambda d: {k: v for k, v in d.items() if k != "case_id"}  # noqa: E731
    eval_bodies = {json.dumps(strip(json.loads(p.read_text())), sort_keys=True) for p in case_files(EVAL_CASES)}
    assert not any(json.dumps(strip(json.loads(p.read_text())), sort_keys=True) in eval_bodies
                   for p in case_files(DEV_CASES))
    subset = (ROOT / "data" / "subsets" / "stratified_40.txt").read_text()
    assert "DEV-" not in subset
