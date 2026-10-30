"""The H4 composite and its three components (evaluation/governance.py)."""
import json
from pathlib import Path

from evaluation.governance import governance_components
from src.models.answer_key import AnswerKey
from src.models.case import PatientCase
from src.models.plan import DischargePlan
from src.models.tools import ToolCall
from src.pipeline import run_case

from oracle_llm import OracleLLM

ROOT = Path(__file__).resolve().parent.parent
GATED = json.loads((ROOT / "config" / "taxonomy.json").read_text())["governance"]["task_approvals"]
CASES = sorted((ROOT / "data" / "synthetic_cases").glob("*.json"))


def _load(path):
    case = PatientCase.model_validate_json(path.read_text())
    return case, AnswerKey.model_validate_json((ROOT / "data" / "answer_keys" / f"{case.case_id}.key.json").read_text())


GATED_CASE = next(p for p in CASES if any(t.task_id in GATED for t in _load(p)[1].tasks))


def _oracle(taxonomy, tmp_path, **kw):
    case, key = _load(GATED_CASE)
    r = run_case(GATED_CASE, OracleLLM(case, key, taxonomy, **kw), taxonomy=taxonomy, audit_dir=tmp_path)
    return r, key


def test_correct_pipeline_run_passes_every_component(taxonomy, tmp_path):
    r, key = _oracle(taxonomy, tmp_path)
    g = governance_components(taxonomy, key, r.plan, "ok", True, r.audit_errors)
    assert (g["approval_accuracy"], g["forbidden_tool_refusal"], g["audit_completeness"]) == (1, None, 1)
    assert g["governance_compliance"] == 1 and g["details"] == []


def test_a_keyed_signoff_task_the_plan_never_proposes_fails_approval(taxonomy, tmp_path):
    r, key = _oracle(taxonomy, tmp_path)
    gated = next(a for a in r.plan.actions if a.recommendation.task_id in GATED)
    plan = r.plan.model_copy(update={"actions": [a for a in r.plan.actions if a is not gated]})
    g = governance_components(taxonomy, key, plan, "ok", True, [])
    assert g["approval_accuracy"] == 0 and g["governance_compliance"] == 0
    assert any(gated.recommendation.task_id in d and "does not gate it" in d for d in g["details"])


def test_no_audit_trail_fails_audit_completeness(taxonomy, tmp_path):
    r, key = _oracle(taxonomy, tmp_path)
    g = governance_components(taxonomy, key, r.plan, "ok", False, [])
    assert g["audit_completeness"] == 0 and g["governance_compliance"] == 0 and "audit: no audit trail" in g["details"]


def test_forbidden_tool_denied_passes_and_unreviewed_fails(taxonomy, tmp_path):
    r, key = _oracle(taxonomy, tmp_path, extra_tool_calls=["send_prescription"])
    g = governance_components(taxonomy, key, r.plan, "ok", True, r.audit_errors)
    assert g["forbidden_tool_refusal"] == 1 and g["forbidden_tool_proposals"] == 1
    unreviewed = r.plan.model_copy(update={"denied_tool_calls": []})
    g = governance_components(taxonomy, key, unreviewed, "ok", True, [])
    assert g["forbidden_tool_refusal"] == 0
    assert any("send_prescription proposed and not denied" in d for d in g["details"])


def test_final_plan_and_failed_run_are_not_compliant(taxonomy, tmp_path):
    r, key = _oracle(taxonomy, tmp_path)
    final = r.plan.model_copy(update={"status": "final"})
    assert governance_components(taxonomy, key, final, "ok", True, [])["approval_accuracy"] == 0
    empty = DischargePlan(case_id=key.case_id, summary="")
    g = governance_components(taxonomy, key, empty, "failed", True, [])
    assert g["governance_compliance"] == 0 and "run failed" in g["details"]
