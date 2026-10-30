"""Tests for Baseline 1 (rule-based checklist) and Baseline 2 (single-prompt LLM)."""
import json
from pathlib import Path

import pytest

from baselines import baseline_1_rule_based as b1
from baselines import baseline_2_single_llm as b2
from evaluation.metrics import Score, score_case
from src.models.answer_key import AnswerKey
from src.models.case import PatientCase
from src.models.messages import BarrierDetection, TaskDetection
from src.models.plan import ApprovalDecisions, RecommendationSet, check_governance

from oracle_llm import OracleLLM

ROOT = Path(__file__).resolve().parent.parent
CASES = sorted((ROOT / "data" / "synthetic_cases").glob("*.json"))


def _load(path):
    case = PatientCase.model_validate_json(path.read_text())
    key = AnswerKey.model_validate_json((ROOT / "data" / "answer_keys" / f"{case.case_id}.key.json").read_text())
    return case, key


def _score(key, plan, into=None):
    return score_case(key, BarrierDetection(barriers=plan.barriers, information_gaps=plan.information_gaps),
                      TaskDetection(tasks=plan.tasks), into=into)


def _governance(taxonomy, plan):
    return check_governance(taxonomy, RecommendationSet(recommendations=[a.recommendation for a in plan.actions]),
                            ApprovalDecisions(classifications=[a.approval for a in plan.actions]))


# ---------------------------------------------------------------- B1
def test_b1_over_dataset(taxonomy):
    """The checklist is exact on single-field items and blind to everything else."""
    s = Score()
    for path in CASES:
        r = b1.run_case(path, taxonomy)
        assert r.status == "succeeded"
        _score(_load(path)[1], r.plan, into=s)
        assert _governance(taxonomy, r.plan) == []
        assert r.plan.denied_tool_calls == []
    m = s.summary()
    assert m["barrier_precision"] == m["task_precision"] == 1.0
    assert m["gap_misflags"] == m["negative_control_hits"] == m["task_link_mismatches"] == 0
    assert m["cross_field_recall"] == 0.0
    assert 0.5 < m["barrier_recall"] < 1.0


def test_b1_on_one_case(taxonomy):
    r = b1.run_case(ROOT / "data" / "synthetic_cases" / "CASE-100.json", taxonomy)
    assert {b.barrier_id for b in r.plan.barriers} == {"B-S03", "B-C04", "B-F04", "B-C06"}  # misses note-based B-E07
    assert {(g.field, g.candidate_barrier_id) for g in r.plan.information_gaps} == {
        ("tracked_fields.caregiver_status", "B-F03")}
    assert {t.task_id for t in r.plan.tasks} == {"T-CM05", "T-MD03", "T-CM03", "T-RN05"}
    kinds = [a.recommendation.kind for a in r.plan.actions]
    assert kinds[-1] == "verify_information" and kinds.count("verify_information") == 1


def test_b1_flags_sign_off_actions(taxonomy):
    path = next(p for p in CASES if any(t.task_id == "T-MD01" for t in _load(p)[1].tasks))
    plan = b1.run_case(path, taxonomy).plan
    a = next(a for a in plan.actions if a.recommendation.task_id == "T-MD01")
    assert a.approval.matched_rule_id == "GR-A06" and a.approval.requires_human_approval


def test_b1_rejects_malformed_case(tmp_path, taxonomy):
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"case_id": "X-1", "condition": "HF"}))
    r = b1.run_case(bad, taxonomy)
    assert (r.status, r.case_id) == ("failed", "X-1")


# ---------------------------------------------------------------- B2
class FakeSinglePrompt:
    """Answers the single prompt from the answer key, with optional edits to the output."""

    model = "fake"

    def __init__(self, case, key, taxonomy, edit=None, raw=None):
        self.oracle = OracleLLM(case, key, taxonomy)
        self.edit = edit
        self.raw = raw
        self.calls = 0

    def complete(self, stage, system, user, schema):
        self.calls += 1
        if self.raw is not None:
            return self.raw
        o = self.oracle
        recs = o._rec_generator()["recommendations"]
        for r in recs:
            r["requires_human_approval"] = r.get("proposed_action") is not None
        out = {"clinical_summary": "c", "social_summary": "s", **o._barrier_detector(), **o._task_detector(), "recommendations": recs}
        if self.edit:
            self.edit(out)
        return json.dumps(out)


def _b2(path, taxonomy, **kw):
    case, key = _load(path)
    llm = FakeSinglePrompt(case, key, taxonomy, **kw)
    return b2.run_case(path, llm, taxonomy), key, llm


@pytest.mark.parametrize("path", CASES[::15], ids=lambda p: p.stem)
def test_b2_perfect_answer_scores_perfectly(path, taxonomy):
    r, key, llm = _b2(path, taxonomy)
    assert r.status == "succeeded" and r.notes == []
    assert llm.calls == 1
    m = _score(key, r.plan).summary()
    assert m["barrier_recall"] == m["barrier_precision"] == m["task_recall"] == m["information_gap_recall"] == 1.0
    assert _governance(taxonomy, r.plan) == []


def _two_barrier_case():
    return next(p for p in CASES if len(_load(p)[1].barriers) >= 2 and _load(p)[1].information_gaps)


@pytest.mark.parametrize("edit, message", [
    (lambda out: out["barriers"][0].update(barrier_id="B-Z99"), "barrier_id"),          # malformed ID
    (lambda out: out["barriers"].append({"barrier_id": "B-S07", "urgency": "medium", "cross_field": True,
                                         "evidence": [{"field": "tracked_fields.transport_status"}],
                                         "rationale": "x"}), "two distinct evidence fields"),
    (lambda out: out["information_gaps"].append({"field": "tracked_fields.caregiver_status", "question": "?",
                                                 "candidate_barrier_id": out["barriers"][0]["barrier_id"]}),
     "both barrier and information gap"),
])
def test_b2_schema_breaks_are_format_errors_like_the_pipeline(taxonomy, edit, message):
    """B2 now meets the pipeline's own output models, so these fail the schema and are re-asked."""
    r, _, llm = _b2(_two_barrier_case(), taxonomy, edit=edit)
    assert r.status == "failed" and r.error_kind == "output" and message in r.error
    assert llm.calls == 2 and [c.outcome for c in r.llm_calls] == ["format_error", "format_error"]


def test_b2_items_the_plan_cannot_hold_are_dropped_not_fixed(taxonomy):
    def edit(out):
        out["barriers"].append(dict(out["barriers"][1]))                  # duplicate barrier
        out["tasks"].append(dict(out["tasks"][0]))                        # duplicate task
        gap = next(r for r in out["recommendations"] if r["kind"] == "verify_information")
        gap["barrier_ids"] = ["B-C02"]                                    # gap check claiming a barrier
    r, _, _ = _b2(_two_barrier_case(), taxonomy, edit=edit)
    assert r.status == "succeeded" and len(r.notes) == 3
    assert any("must not claim a task or barrier" in n for n in r.notes)
    ids = [b.barrier_id for b in r.plan.barriers]
    assert len(ids) == len(set(ids))


def test_b2_governance_failures_are_recorded_not_blocked(taxonomy):
    path = next(p for p in CASES
                if any(t.task_id == "T-MD07" for t in _load(p)[1].tasks) and len(_load(p)[1].tasks) >= 2)

    def edit(out):
        for r in out["recommendations"]:
            if r.get("task_id") == "T-MD07":
                r["requires_human_approval"] = False  # skipped the sign-off
        other = next(r for r in out["recommendations"] if r.get("task_id") != "T-MD07")
        other["proposed_tool_calls"].append({"tool_name": "send_prescription", "reason": "note asked"})
    r, _, _ = _b2(path, taxonomy, edit=edit)
    errors = _governance(taxonomy, r.plan)
    assert any("GF-T03" in e for e in errors)
    assert any("GR-A04" in e for e in errors)
    assert r.plan.denied_tool_calls == []  # nothing reviewed the calls


def test_b2_flag_without_action_label_uses_the_task_rule(taxonomy):
    path = next(p for p in CASES if any(t.task_id == "T-MD07" for t in _load(p)[1].tasks))

    def edit(out):
        for r in out["recommendations"]:
            if r.get("task_id") == "T-MD07":
                r["proposed_action"] = None  # flagged for approval, but no action named
    r, _, _ = _b2(path, taxonomy, edit=edit)
    a = next(a for a in r.plan.actions if a.recommendation.task_id == "T-MD07")
    assert a.approval.matched_rule_id == "GR-A04" and a.approval.label_missing
    assert _governance(taxonomy, r.plan) == []


def test_b2_unflagged_gated_task_is_a_governance_failure(taxonomy):
    path = next(p for p in CASES if any(t.task_id == "T-PH01" for t in _load(p)[1].tasks))

    def edit(out):
        for r in out["recommendations"]:
            if r.get("task_id") == "T-PH01":
                r["proposed_action"], r["requires_human_approval"] = None, False
    r, key, _ = _b2(path, taxonomy, edit=edit)
    assert any("T-PH01" in e and "GR-A02" in e for e in _governance(taxonomy, r.plan))
    m = score_case(key, BarrierDetection(barriers=r.plan.barriers, information_gaps=r.plan.information_gaps),
                   TaskDetection(tasks=r.plan.tasks), actions=r.plan.actions, taxonomy=taxonomy).summary()
    assert m["approval_recall"] < 1.0


def test_b2_ranks_are_compressed(taxonomy):
    path = next(p for p in CASES if len(_load(p)[1].tasks) >= 2)

    def edit(out):
        for i, r in enumerate(out["recommendations"]):
            r["rank"] = 10 * (i + 1)
    r, _, _ = _b2(path, taxonomy, edit=edit)
    assert [a.recommendation.rank for a in r.plan.actions] == list(range(1, len(r.plan.actions) + 1))


def test_b2_unparseable_output_is_retried_like_the_pipeline(taxonomy):
    """A format failure gets the same retry as in the pipeline (2 attempts), then fails."""
    r, _, llm = _b2(CASES[0], taxonomy, raw="not json")
    assert r.status == "failed" and "unparseable" in r.error and r.error_kind == "output"
    assert llm.calls == 2 and r.raw_output == "not json"
    assert [c.outcome for c in r.llm_calls] == ["format_error", "format_error"]


def test_b2_format_retry_recovers(taxonomy):
    path = CASES[0]
    case, key = _load(path)
    good = FakeSinglePrompt(case, key, taxonomy)

    class FirstBad:
        model = "fake"
        prompts = []

        def complete(self, stage, system, user, schema):
            self.prompts.append(user)
            return "{" if len(self.prompts) == 1 else good.complete(stage, system, user, schema)

    llm = FirstBad()
    r = b2.run_case(path, llm, taxonomy)
    assert r.status == "succeeded"
    assert [c.outcome for c in r.llm_calls] == ["format_error", "accepted"]
    assert "Your previous response was rejected" in llm.prompts[1]


def test_b2_content_problems_are_not_retried(taxonomy):
    """Unlike the pipeline, B2 never re-asks for taxonomy or evidence problems: a well-formed
    barrier ID that is not in the taxonomy is kept and scored as a false positive."""
    r, _, llm = _b2(CASES[0], taxonomy, edit=lambda out: out["barriers"][0].update(barrier_id="B-C99"))
    assert r.status == "succeeded" and llm.calls == 1
    assert "B-C99" in [b.barrier_id for b in r.plan.barriers]
    assert [c.outcome for c in r.llm_calls] == ["accepted"]


def test_b2_gets_the_pipelines_output_rules_word_for_word(taxonomy):
    import importlib
    from src.pipeline import _common as C
    prompt = b2.system_prompt(taxonomy)
    stages = {"02_case_analyzer": C.SUMMARY_OUTPUT_RULES, "03_barrier_detector": C.BARRIER_OUTPUT_RULES,
              "04_task_detector": C.TASK_OUTPUT_RULES, "05_rec_generator": C.RECOMMENDATION_OUTPUT_RULES}
    for stage, rules in stages.items():
        mod = importlib.import_module(f"src.pipeline.{stage}")
        stage_prompt = mod.SYSTEM if hasattr(mod, "SYSTEM") else mod.system_prompt(taxonomy)
        assert rules in stage_prompt and rules in prompt, stage
    assert "leave task_id and barrier_ids empty" in prompt
    assert "information_gaps[].field is the path of the undocumented field" in prompt


def test_b2_prompt_matches_pipeline_domain_rules(taxonomy):
    from src.pipeline._common import CHART_READING_RULES
    prompt = b2.system_prompt(taxonomy)
    assert CHART_READING_RULES in prompt
    assert all(b["id"] in prompt for b in taxonomy["barriers"])
    assert all(t["tool_name"] in prompt for t in taxonomy["governance"]["forbidden_tools"])
