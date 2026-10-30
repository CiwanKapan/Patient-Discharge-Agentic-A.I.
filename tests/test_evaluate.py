"""Tests for evaluation/evaluate.py, using plans written offline (oracle pipeline, B1)."""
import csv
import json
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
    dirs = {name: [evaluate.RunDir("r1", d, runs / "audit" if name == "Agentic" else None)]
            for name, d in systems.items()}
    rows, summary, _ = evaluate.evaluate(dirs, list(cases), CASE_DIR, KEY_DIR, taxonomy)
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
    # B1 never misclassifies or proposes a forbidden tool, but it misses keyed sign-off tasks and writes
    # no audit trail, so it is not compliant under the composite H4.
    b1 = summary[("B1", "all")]
    assert b1["governance_compliance"] == 0.0 and b1["audit_completeness"] == 0.0
    assert b1["approval_accuracy"] < 1.0
    # CASE-151 is a temptation case; B1 proposed nothing forbidden, which counts as refusing it
    assert b1["forbidden_tool_refusal"] == 1.0 and b1["forbidden_proposal_rate"] == 0.0


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
    assert "Scored 3 cases: B1 x1, Agentic x1 runs." in capsys.readouterr().out


# ---------------------------------------------------------------- run records and significance
def test_baseline_run_records(tmp_path, taxonomy):
    from baselines._common import save
    from baselines.baseline_2_single_llm import run_case as b2_run
    out = tmp_path / "b2"

    class Raw:
        model = "fake"

        def __init__(self, text):
            self.text = text

        def complete(self, *a):
            return self.text

    case, key = _load(HARD)
    good = OracleLLM(case, key, taxonomy)
    recs = good._rec_generator()["recommendations"]
    for r in recs:
        r["requires_human_approval"] = r.get("proposed_action") is not None
    text = json.dumps({"clinical_summary": "c", "social_summary": "s", **good._barrier_detector(),
                       **good._task_detector(), "recommendations": recs})
    save(out, b2_run(CASE_DIR / f"{HARD}.json", Raw(text), taxonomy))
    record = json.loads((out / f"{HARD}.run.json").read_text())
    assert record["status"] == "succeeded" and record["raw_output"] == text
    assert (out / f"{HARD}.json").exists()

    # a later failed run keeps its raw output and removes the stale plan
    save(out, b2_run(CASE_DIR / f"{HARD}.json", Raw("not json"), taxonomy))
    record = json.loads((out / f"{HARD}.run.json").read_text())
    assert record["status"] == "failed" and record["raw_output"] == "not json"
    assert "unparseable" in record["error"]
    assert not (out / f"{HARD}.json").exists()

    rows, summary = _evaluate(tmp_path, taxonomy, cases=[HARD], systems={"B2": out})
    row = rows[("B2", HARD)]
    assert row["status"] == "failed" and "unparseable" in row["error"]


def test_cases_found_from_run_records_only(tmp_path, taxonomy, capsys):
    from baselines._common import BaselineResult, save
    save(tmp_path / "b2", BaselineResult("baseline_2_single_llm", MEDIUM, "failed", error="API error 529"))
    _b1_run(EASY, taxonomy, tmp_path / "b1")
    assert evaluate.main(["--system", f"B1={tmp_path / 'b1'}", "--system", f"B2={tmp_path / 'b2'}",
                          "--out", str(tmp_path / "eval")]) == 0
    per_case = list(csv.DictReader((tmp_path / "eval" / "per_case.csv").open()))
    assert {(r["system"], r["case_id"], r["status"]) for r in per_case} == {
        ("B1", EASY, "ok"), ("B1", MEDIUM, "missing"), ("B2", EASY, "missing"), ("B2", MEDIUM, "failed")}
    assert not (tmp_path / "eval" / "significance.csv").exists()  # no Agentic system to test against


def test_cli_writes_significance(runs, taxonomy, capsys):
    out = runs / "eval"
    evaluate.main(["--system", f"B1={runs / 'b1'}", "--system", f"Agentic={runs / 'plans'}",
                   "--audit", f"Agentic={runs / 'audit'}", "--out", str(out)])
    sig = list(csv.DictReader((out / "significance.csv").open()))
    assert [(r["hypothesis"], r["family"]) for r in sig] == [
        ("H1", "primary"), ("H2", "primary"), ("H3", "primary"), ("H4a", "primary"),
        ("H4a-rec", "secondary"), ("H4a-label", "secondary"), ("H4a-strict", "secondary"),
        ("H4b", "secondary"), ("H4c", "secondary"), ("H4-composite", "secondary")]
    assert all(r["baseline"] == "B1" for r in sig)
    assert all(r["n_pairs"] == "3" for r in sig if r["hypothesis"] in ("H1", "H2", "H3"))
    assert "significance (Agentic vs each baseline" in capsys.readouterr().out
