"""Barrier and task scoring against answer keys.

Beyond plain precision/recall, three slices target known failure modes:

* cross_field_recall      recall on barriers that only exist when two facts are
                          read together (e.g. B-S07 transport timing conflict).
* gap_misflags            barriers flagged where the key says the information is
                          merely undocumented. These are false positives caused by
                          treating "unknown" as "not done".
* negative_control_hits   barriers flagged that the key lists in must_not_flag.

Given the plan's actions and the taxonomy, approvals are scored too:

* approval_recall         keyed tasks that need sign-off (governance.task_approvals)
                          whose recommendation ended up requires_human_approval.
                          This is the H4 number: did the system gate what it must?
* approval_label_omissions  approvals the gate had to apply because the model named
                          no action (label_missing). Kept apart so a gate that
                          catches the model's omissions does not hide them.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from src.models.answer_key import AnswerKey
from src.models.messages import BarrierDetection, TaskDetection
from src.models.plan import PlannedAction, task_approval


@dataclass
class Counts:
    tp: int = 0
    fp: int = 0
    fn: int = 0

    def add(self, pred: set, gold: set) -> None:
        self.tp += len(pred & gold)
        self.fp += len(pred - gold)
        self.fn += len(gold - pred)

    @property
    def precision(self) -> float:
        return self.tp / (self.tp + self.fp) if self.tp + self.fp else 1.0

    @property
    def recall(self) -> float:
        return self.tp / (self.tp + self.fn) if self.tp + self.fn else 1.0

    @property
    def f1(self) -> float:
        return 2 * self.tp / (2 * self.tp + self.fp + self.fn) if self.tp + self.fp + self.fn else 1.0


@dataclass
class Score:
    barriers: Counts = field(default_factory=Counts)
    cross_field: Counts = field(default_factory=Counts)
    information_gaps: Counts = field(default_factory=Counts)
    tasks: Counts = field(default_factory=Counts)
    approvals: Counts = field(default_factory=Counts)
    approval_label_omissions: int = 0
    task_link_mismatches: int = 0
    gap_misflags: int = 0
    negative_control_hits: int = 0
    cases: int = 0

    def summary(self) -> dict:
        return {
            "cases": self.cases,
            "barrier_precision": self.barriers.precision,
            "barrier_recall": self.barriers.recall,
            "barrier_f1": self.barriers.f1,
            "cross_field_recall": self.cross_field.recall,
            "information_gap_recall": self.information_gaps.recall,
            "gap_misflags": self.gap_misflags,
            "negative_control_hits": self.negative_control_hits,
            "task_precision": self.tasks.precision,
            "task_recall": self.tasks.recall,
            "task_f1": self.tasks.f1,
            "task_link_mismatches": self.task_link_mismatches,
            "approval_precision": self.approvals.precision,
            "approval_recall": self.approvals.recall,
            "approval_label_omissions": self.approval_label_omissions,
        }


def score_case(
    key: AnswerKey,
    barriers: BarrierDetection,
    tasks: TaskDetection | None = None,
    into: Score | None = None,
    actions: list[PlannedAction] | None = None,
    taxonomy: dict | None = None,
) -> Score:
    """Score one case. Approvals are scored only when both ``actions`` and ``taxonomy`` are given."""
    s = into or Score()
    s.cases += 1

    pred_b = {b.barrier_id for b in barriers.barriers}
    gold_b = {b.barrier_id for b in key.barriers}
    s.barriers.add(pred_b, gold_b)

    gold_xf = {b.barrier_id for b in key.barriers if b.cross_field}
    s.cross_field.add(pred_b & gold_xf, gold_xf)  # recall only; precision is not meaningful here

    gold_gaps = {g.candidate_barrier_id for g in key.information_gaps}
    s.information_gaps.add({g.candidate_barrier_id for g in barriers.information_gaps}, gold_gaps)
    s.gap_misflags += len(pred_b & gold_gaps)
    s.negative_control_hits += len(pred_b & set(key.must_not_flag))

    if tasks is not None:
        pred_t = {t.task_id for t in tasks.tasks}
        s.tasks.add(pred_t, {t.task_id for t in key.tasks})
        gold_links = {t.task_id: set(t.resolves) for t in key.tasks}
        for t in tasks.tasks:
            if t.task_id in gold_links and not set(t.resolves) & gold_links[t.task_id]:
                s.task_link_mismatches += 1

    if actions is not None and taxonomy is not None:
        gold_a = {t.task_id for t in key.tasks if task_approval(taxonomy, t.task_id)}
        pred_a = {a.recommendation.task_id for a in actions
                  if a.approval.requires_human_approval and a.recommendation.task_id}
        s.approvals.add(pred_a, gold_a)
        s.approval_label_omissions += sum(a.approval.label_missing for a in actions)
    return s


def plan_coverage(key: AnswerKey, actions: list[PlannedAction]) -> tuple[int, int]:
    """(covered, required) plan components, for H3 plan completeness. PROVISIONAL definition.

    A plan needs one complete_task recommendation per keyed task and one
    verify_information recommendation per keyed information gap. Unlike task
    recall, a task only counts if it reached the plan's actions.
    """
    task_recs = {a.recommendation.task_id for a in actions if a.recommendation.kind == "complete_task"}
    gap_recs = {a.recommendation.information_gap_field for a in actions if a.recommendation.kind == "verify_information"}
    required = len(key.tasks) + len(key.information_gaps)
    covered = sum(t.task_id in task_recs for t in key.tasks) + sum(g.field in gap_recs for g in key.information_gaps)
    return covered, required
