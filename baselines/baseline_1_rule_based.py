"""Baseline 1 - rule-based checklist.

A static checklist that validates each tracked field on its own, with no
reading of free-text notes and no comparison between fields:

    in_progress / not_started   -> the barrier the taxonomy ties to that field
    unknown / absent            -> an information gap for that barrier
    complete / not_applicable   -> nothing

Each barrier gets the task that names the same evidence field, each item gets a
recommendation, and a fixed table attaches the sign-off action for tasks that
need one. By design it cannot find cross-field barriers (B-S07, B-E07),
barriers that only a note reveals, or the B-S07 gap of a pickup with no time.

    python -m baselines.baseline_1_rule_based data/synthetic_cases/ --out runs/b1
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

from baselines._common import BaselineResult, load_case, main
from src.models.case import FieldReading, PatientCase, read_field
from src.models.messages import BarrierFinding, EvidenceRef, InformationGap, TaskFinding
from src.models.plan import DischargePlan, PlannedAction, Recommendation, task_approval
from src.pipeline._common import load_taxonomy

approval_gate = importlib.import_module("src.pipeline.06_approval_gate")

SYSTEM = "baseline_1_rule_based"

URGENCY_RANK = {"high": 1, "medium": 2, "low": 3}


def _field_rules(taxonomy: dict, condition: str) -> dict[str, dict]:
    """Field name -> the single-field barrier it signals for this condition.

    A field shared by several barriers maps to the first one listed.
    """
    rules = {}
    for b in taxonomy["barriers"]:
        if b["cross_field"] or condition not in b["conditions"]:
            continue
        for f in b["evidence_fields"]:
            rules.setdefault(f, b)
    return rules


def _task_for(taxonomy: dict, condition: str, barrier_id: str, field: str) -> dict | None:
    """The task that resolves ``barrier_id``, preferring one that names the same field."""
    candidates = [t for t in taxonomy["tasks"] if barrier_id in t["resolves"] and condition in t["conditions"]]
    same_field = [t for t in candidates if field in t["evidence_fields"]]
    return (same_field or candidates or [None])[0]


def plan_for(case: PatientCase, taxonomy: dict) -> DischargePlan:
    barriers, gaps, tasks, recs = [], [], [], []
    for field, b in _field_rules(taxonomy, case.condition).items():
        f = case.field(field)
        reading = read_field(f)
        path = f"tracked_fields.{field}"
        if reading is FieldReading.MISSING:
            gaps.append(InformationGap(field=path, candidate_barrier_id=b["id"], question=f"Is {field} documented?"))
            recs.append(dict(kind="verify_information", description=f"Confirm and document {field}.",
                             urgency="medium", owner_role="case_manager", information_gap_field=path, sort=4))
        elif reading is FieldReading.INCOMPLETE:
            evidence = [EvidenceRef(field=path, status=f.status, quote=f.detail)]
            barriers.append(BarrierFinding(barrier_id=b["id"], urgency=b["urgency"], cross_field=False,
                                           evidence=evidence, rationale=f"{field} is {f.status.value}."))
            t = _task_for(taxonomy, case.condition, b["id"], field)
            if t is None:
                continue
            tasks.append(TaskFinding(task_id=t["id"], resolves=[b["id"]], owner_role=t["owner_roles"][0],
                                     urgency=t["urgency"], evidence=evidence, rationale=f"Resolves {b['id']}."))
            recs.append(dict(kind="complete_task", description=t["name"], urgency=t["urgency"],
                             owner_role=t["owner_roles"][0], task_id=t["id"], barrier_ids=[b["id"]],
                             proposed_action=(task_approval(taxonomy, t["id"]) or {}).get("action"), sort=URGENCY_RANK[t["urgency"]]))

    recs.sort(key=lambda r: r["sort"])
    dense = {s: i for i, s in enumerate(sorted({r["sort"] for r in recs}), 1)}
    actions = []
    for i, r in enumerate(recs, 1):
        rec = Recommendation(recommendation_id=f"R{i}", rank=dense[r.pop("sort")], **r)
        actions.append(PlannedAction(recommendation=rec, approval=approval_gate.classify(taxonomy, rec)))

    return DischargePlan(
        case_id=case.case_id,
        summary=f"Checklist review: {len(barriers)} incomplete items, {len(gaps)} undocumented items.",
        barriers=barriers,
        information_gaps=gaps,
        tasks=tasks,
        actions=actions,
    )


def run_case(path: str | Path, taxonomy: dict | None = None) -> BaselineResult:
    case, failed = load_case(path, SYSTEM)
    if failed:
        return failed
    return BaselineResult(SYSTEM, case.case_id, "succeeded", plan=plan_for(case, taxonomy or load_taxonomy()))


if __name__ == "__main__":
    sys.exit(main(SYSTEM, run_case))
