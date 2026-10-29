"""Tests for evaluation/evaluate.py, using plans written offline (oracle pipeline, B1)."""
import csv
from pathlib import Path

import pytest

from baselines import baseline_1_rule_based as b1
from evaluation import evaluate
from src.models.answer_key import AnswerKey
from src.models.case import PatientCase
from src.models.messages import Stage
from src.models.plan import DischargePlan
from src.pipeline import run_case

from oracle_llm import OracleLLM, ScriptedLLM

ROOT = Path(__file__).resolve().parent.parent
CASE_DIR = ROOT / "data" / "synthetic_cases"
KEY_DIR = ROOT / "data" / "answer_keys"
# one case per difficulty, the first with a gated task and the hard one with a cross-field barrier
EASY, MEDIUM, HARD = "CASE-152", "CASE-154", "CASE-151"


def _load(cid):
    case = PatientCase.model_validate_json((CASE_DIR / f"{cid}.json").read_text())
    return case, AnswerKey.model_validate_json((KEY_DIR / f"{cid}.key.json").read_text())


def _oracle_run(cid, taxonomy, plans, audit, llm=None):
    case, key = _load(cid)
    r = run_case(CASE_DIR / f"{cid}.json", llm or OracleLLM(case, key, taxonomy), taxonomy=taxonomy, audit_dir=audit)
    if r.plan:
        plans.mkdir(parents=True, exist_ok=True)
        (plans / f"{cid}.json").write_text(r.plan.model_dump_json())
    return r


def _b1_run(cid, taxonomy, plans):
    plans.mkdir(parents=True, exist_ok=True)
    r = b1.run_case(CASE_DIR / f"{cid}.json", taxonomy)
    (plans / f"{cid}.json").write_text(r.plan.model_dump_json())


@pytest.fixture
def runs(tmp_path, taxonomy):
    for cid in (EASY, MEDIUM, HARD):
        _oracle_run(cid, taxonomy, tmp_path / "plans", tmp_path / "audit")
        _b1_run(cid, taxonomy, tmp_path / "b1")
    return tmp_path


def _evaluate(runs, taxonomy, cases=(EASY, MEDIUM, HARD), systems=None):
    systems = systems or {"B1": runs / "b1", "Agentic": runs / "plans"}
    rows, summary = evaluate.evaluate(systems, {"Agentic": runs / "audit"}, list(cases), CASE_DIR, KEY_DIR, taxonomy)
    return {(r["system"], r["case_id"]): r for r in rows}, {(r["system"], r["slice"]): r for r in summary}


def test_oracle_plans_score_perfectly(runs, taxonomy):
    rows, summary = _evaluate(runs, taxonomy)
    s = summary[("Agentic", "all")]
    for k in ("barrier_recall", "barrier_precision", "cross_field_recall", "information_gap_recall",
              "task_recall", "task_precision", "plan_completeness", "approval_recall", "governance_compliance"):
        assert s[k] == 1.0, k
    assert s["failed"] == s["governance_violations"] == s["approval_label_omissions"] == 0
    assert s["cases"] == 3
    assert all(rows[("Agentic", c)]["status"] == "ok" for c in (EASY, MEDIUM, HARD))


def test_b1_misses_what_it_cannot_see(runs, taxonomy):
    rows, summary = _evaluate(runs, taxonomy)
    assert rows[("B1", MEDIUM)]["barriers_missed"] == "B-S02"   # note-only
    assert rows[("B1", HARD)]["barriers_missed"] == "B-E07"     # cross-field
    assert summary[("B1", "difficulty=hard")]["cross_field_recall"] == 0.0
    assert summary[("B1", "all")]["governance_compliance"] == 1.0


def test_nothing_to_count_is_blank_not_one(runs, taxonomy):
    rows, summary = _evaluate(runs, taxonomy)
    easy = summary[("Agentic", "difficulty=easy")]
    assert easy["cross_field_recall"] is None and easy["information_gap_recall"] is None
    assert rows[("Agentic", EASY)]["approval_recall"] is None
    assert easy["barrier_recall"] == 1.0


def test_missing_plan_is_scored_as_empty(runs, taxonomy):
    (runs / "b1" / f"{HARD}.json").unlink()
    rows, summary = _evaluate(runs, taxonomy)
    assert rows[("B1", HARD)]["status"] == "missing"
    assert rows[("B1", HARD)]["barrier_recall"] == 0.0
    assert summary[("B1", "all")]["failed"] == 1
    assert summary[("B1", "all")]["cases"] == 3


def test_failed_pipeline_run_reports_its_error(tmp_path, taxonomy):
    case, key = _load(MEDIUM)
    oracle = OracleLLM(case, key, taxonomy)
    llm = ScriptedLLM(oracle, {Stage.CASE_ANALYZER: ["not json", "not json"]})
    r = _oracle_run(MEDIUM, taxonomy, tmp_path / "plans", tmp_path / "audit", llm=llm)
    assert r.status == "failed"
    rows, summary = _evaluate(tmp_path, taxonomy, cases=[MEDIUM], systems={"Agentic": tmp_path / "plans"})
    row = rows[("Agentic", MEDIUM)]
    assert row["status"] == "failed" and "02_case_analyzer" in row["error"]
    assert summary[("Agentic", "all")]["failed"] == 1


def test_governance_violation_is_counted(runs, taxonomy):
    path = runs / "plans" / f"{HARD}.json"
    plan = DischargePlan.model_validate_json(path.read_text())
    gated = next(a for a in plan.actions if a.approval.requires_human_approval)
    rule = gated.approval.matched_rule_id
    gated.approval = gated.approval.model_copy(update={
        "classification": "auto_safe", "requires_human_approval": False, "matched_rule_id": None})
    path.write_text(plan.model_dump_json())
    rows, summary = _evaluate(runs, taxonomy)
    assert rows[("Agentic", HARD)]["governance_violations"] >= 1
    details = rows[("Agentic", HARD)]["violation_details"]
    assert gated.recommendation.recommendation_id in details and rule in details
    assert summary[("Agentic", "all")]["governance_compliance"] == pytest.approx(2 / 3, abs=1e-4)


def test_cli_writes_both_csvs(runs, taxonomy, capsys):
    out = runs / "eval"
    code = evaluate.main(["--system", f"B1={runs / 'b1'}", "--system", f"Agentic={runs / 'plans'}",
                          "--audit", f"Agentic={runs / 'audit'}", "--out", str(out)])
    assert code == 0
    per_case = list(csv.DictReader((out / "per_case.csv").open()))
    summary = list(csv.DictReader((out / "summary.csv").open()))
    assert len(per_case) == 6
    assert {r["slice"] for r in summary} >= {"all", "difficulty=easy", "difficulty=medium", "difficulty=hard"}
    assert "Scored 3 cases for B1, Agentic" in capsys.readouterr().out
