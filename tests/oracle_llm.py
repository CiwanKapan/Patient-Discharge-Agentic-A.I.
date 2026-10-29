"""Offline stand-ins for the LLM, used to test the pipeline without API calls.

``OracleLLM`` answers every stage from a case's answer key, so a correct
pipeline run on it must score perfectly and pass every governance and audit
check. ``ScriptedLLM`` returns canned responses per stage, for testing how
stages reject bad output.
"""
from __future__ import annotations

import json
from collections import defaultdict

from src.models.answer_key import AnswerKey
from src.models.case import PatientCase
from src.models.messages import Stage
from src.models.plan import task_approval


class OracleLLM:
    model = "oracle"

    def __init__(self, case: PatientCase, key: AnswerKey, taxonomy: dict, extra_tool_calls=()):
        self.case = case
        self.key = key
        self.barriers = {b["id"]: b for b in taxonomy["barriers"]}
        self.tasks = {t["id"]: t for t in taxonomy["tasks"]}
        self.taxonomy = taxonomy
        self.extra_tool_calls = list(extra_tool_calls)
        self.calls: dict[Stage, int] = defaultdict(int)

    def complete(self, stage, system, user, schema) -> str:
        self.calls[stage] += 1
        return json.dumps(getattr(self, f"_{stage.name.lower()}")())

    def _evidence(self, path: str) -> dict:
        if path.startswith("tracked_fields."):
            f = self.case.field(path.split(".", 1)[1])
            return {"field": path, "status": f.status.value if f else "unknown"}
        return {"field": path}

    def _case_analyzer(self):
        return {"clinical_summary": f"{self.case.condition} patient.", "social_summary": "See chart.",
                "notes_of_interest": []}

    def _barrier_detector(self):
        return {
            "barriers": [
                {"barrier_id": b.barrier_id, "urgency": self.barriers[b.barrier_id]["urgency"],
                 "cross_field": b.cross_field, "evidence": [self._evidence(f) for f in b.evidence_fields],
                 "rationale": "per key"}
                for b in self.key.barriers
            ],
            "information_gaps": [
                {"field": g.field, "candidate_barrier_id": g.candidate_barrier_id, "question": "Confirm?"}
                for g in self.key.information_gaps
            ],
        }

    def _task_detector(self):
        fields = {b.barrier_id: b.evidence_fields for b in self.key.barriers}
        return {"tasks": [
            {"task_id": t.task_id, "resolves": t.resolves, "owner_role": self.tasks[t.task_id]["owner_roles"][0],
             "urgency": self.tasks[t.task_id]["urgency"],
             "evidence": [self._evidence(f) for f in fields[t.resolves[0]]], "rationale": "per key"}
            for t in self.key.tasks
        ]}

    def _rec_generator(self):
        recs = []
        for t in self.key.tasks:
            recs.append({
                "recommendation_id": f"R{len(recs) + 1}", "rank": 1, "kind": "complete_task",
                "description": self.tasks[t.task_id]["name"], "urgency": "high",
                "owner_role": self.tasks[t.task_id]["owner_roles"][0], "task_id": t.task_id,
                "barrier_ids": t.resolves, "proposed_action": (task_approval(self.taxonomy, t.task_id) or {}).get("action"),
                "proposed_tool_calls": [],
            })
        gap_rank = 2 if recs else 1
        for g in self.key.information_gaps:
            recs.append({
                "recommendation_id": f"R{len(recs) + 1}", "rank": gap_rank, "kind": "verify_information",
                "description": f"Confirm {g.field}", "urgency": "medium", "owner_role": "case_manager",
                "information_gap_field": g.field,
                "proposed_tool_calls": [{"tool_name": "flag_for_review", "reason": f"undocumented {g.field}"}],
            })
        if recs and self.extra_tool_calls:
            recs[0]["proposed_tool_calls"] += [{"tool_name": n, "reason": "test"} for n in self.extra_tool_calls]
        return {"recommendations": recs}


class ScriptedLLM:
    """Returns the next canned response for a stage; falls back to ``base`` when none are left."""

    def __init__(self, base, scripts: dict[Stage, list]):
        self.model = getattr(base, "model", "scripted")
        self.base = base
        self.scripts = {s: list(r) for s, r in scripts.items()}

    def complete(self, stage, system, user, schema) -> str:
        queue = self.scripts.get(stage)
        if queue:
            r = queue.pop(0)
            return r if isinstance(r, str) else json.dumps(r)
        return self.base.complete(stage, system, user, schema)
