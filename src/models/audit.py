"""Audit log events (AU-01 .. AU-09), one JSON object per line in a JSONL file.

Every event shares the same header (run, case, sequence, timestamp) and carries
a typed ``details`` object chosen by ``event_type``. ``check_audit_trail``
verifies that a run logged every required event type and that the per-item
events (barriers, tasks, approvals, tool calls, sign-offs) match the plan that was emitted.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Annotated, Any, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, RootModel

from src.models.messages import OwnerRole, Stage, Urgency
from src.models.plan import Classification, DischargePlan, SignoffDecision, gated_actions
from src.models.tools import ToolCall


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _EventBase(_Strict):
    event_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    run_id: str
    case_id: str
    sequence: int = Field(ge=0, description="0 for the first event in a run, then +1 per event.")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    stage: Optional[Stage] = None
    message_id: Optional[str] = Field(None, description="Pipeline message this event came from, if any.")


# ---------------------------------------------------------------- details per event type
class CaseLoadedDetails(_Strict):
    source: str = Field(description="Path or identifier the case was read from.")
    case_sha256: str = Field(pattern=r"^[0-9a-f]{64}$", description="Hash of the raw case file.")
    schema_valid: bool


class ToolCallDetails(_Strict):
    call: ToolCall
    decision: Literal["allowed", "denied"]
    output: Optional[dict[str, Any]] = None
    error: Optional[str] = None


class BarrierFlaggedDetails(_Strict):
    barrier_id: str = Field(pattern=r"^B-[CEFS]\d{2}$")
    evidence_fields: list[str] = Field(min_length=1)
    urgency: Urgency


class TaskRecommendedDetails(_Strict):
    task_id: str = Field(pattern=r"^T-(MD|RN|PH|CM)\d{2}$")
    owner_role: OwnerRole
    linked_barrier_ids: list[str] = Field(min_length=1)


class ApprovalClassificationDetails(_Strict):
    recommendation_id: str
    classification: Classification
    requires_human_approval: bool
    matched_rule_id: Optional[str] = None
    reason: str
    label_missing: bool = False


class PolicyDecisionDetails(_Strict):
    call_id: str
    tool_name: str
    decision: Literal["allowed", "denied"]
    rule_id: Optional[str] = None
    reason: str


class OutputEmittedDetails(_Strict):
    plan: DischargePlan


class LLMCallRecord(_Strict):
    """One model call: which step made it, which attempt it was, how it ended, and its tokens.

    outcome:
      accepted          the response was used
      format_error      it did not parse against the response schema; retried in every LLM arm
      validation_error  it parsed but broke taxonomy or evidence rules; retried by the pipeline only
      llm_error         no usable response (API error, refusal, truncation); never retried
    Token counts are None when the client reports none (offline test clients, failed requests).
    """

    step: str = Field(description="Pipeline stage or baseline name that made the call.")
    attempt: int = Field(ge=1)
    outcome: Literal["accepted", "format_error", "validation_error", "llm_error"]
    errors: list[str] = Field(default_factory=list)
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    cache_read_input_tokens: Optional[int] = None
    cache_creation_input_tokens: Optional[int] = None
    stop_reason: Optional[str] = None
    request_id: Optional[str] = None
    batch: bool = False


class RunCompletedDetails(_Strict):
    status: Literal["succeeded", "failed"]
    model: str = Field(description="Model id used by LLM stages, e.g. claude-sonnet-5-5.")
    prompt_versions: dict[str, str] = Field(description="Prompt version per LLM stage.")
    started_at: datetime
    completed_at: datetime
    tool_call_count: int = Field(
        ge=0,
        description="Number of tool calls the policy layer reviewed in this run, allowed or denied. "
        "Taken from the policy layer, which every tool call must pass through, not from the logger. "
        "Lets the log show on its own that a run made no tool calls.",
    )
    error: Optional[str] = None
    llm_calls: list[LLMCallRecord] = Field(default_factory=list, description="Every model call in the run, in order.")
    llm_settings: Optional[dict[str, Any]] = Field(
        None, description="Model, effort, max_tokens, and max_attempts from config/run_config.json.")


# ---------------------------------------------------------------- one class per AU id
class CaseLoaded(_EventBase):
    audit_id: Literal["AU-01"] = "AU-01"
    event_type: Literal["case_loaded"] = "case_loaded"
    details: CaseLoadedDetails


class ToolCallEvent(_EventBase):
    audit_id: Literal["AU-02"] = "AU-02"
    event_type: Literal["tool_call"] = "tool_call"
    details: ToolCallDetails


class BarrierFlagged(_EventBase):
    audit_id: Literal["AU-03"] = "AU-03"
    event_type: Literal["barrier_flagged"] = "barrier_flagged"
    details: BarrierFlaggedDetails


class TaskRecommended(_EventBase):
    audit_id: Literal["AU-04"] = "AU-04"
    event_type: Literal["task_recommended"] = "task_recommended"
    details: TaskRecommendedDetails


class ApprovalClassified(_EventBase):
    audit_id: Literal["AU-05"] = "AU-05"
    event_type: Literal["approval_classification"] = "approval_classification"
    details: ApprovalClassificationDetails


class PolicyDecisionEvent(_EventBase):
    audit_id: Literal["AU-06"] = "AU-06"
    event_type: Literal["policy_decision"] = "policy_decision"
    details: PolicyDecisionDetails


class OutputEmitted(_EventBase):
    audit_id: Literal["AU-07"] = "AU-07"
    event_type: Literal["output_emitted"] = "output_emitted"
    details: OutputEmittedDetails


class RunCompleted(_EventBase):
    audit_id: Literal["AU-08"] = "AU-08"
    event_type: Literal["run_completed"] = "run_completed"
    details: RunCompletedDetails


class SignoffRecorded(_EventBase):
    audit_id: Literal["AU-09"] = "AU-09"
    event_type: Literal["signoff_recorded"] = "signoff_recorded"
    details: SignoffDecision


AuditEvent = Annotated[
    Union[
        CaseLoaded,
        ToolCallEvent,
        BarrierFlagged,
        TaskRecommended,
        ApprovalClassified,
        PolicyDecisionEvent,
        OutputEmitted,
        RunCompleted,
        SignoffRecorded,
    ],
    Field(discriminator="event_type"),
]


class AuditLogLine(RootModel[AuditEvent]):
    """One line of the JSONL audit log. Use AuditLogLine.model_validate_json(line).root."""


REQUIRED_EVENT_TYPES = (
    "case_loaded",
    "tool_call",
    "barrier_flagged",
    "task_recommended",
    "approval_classification",
    "policy_decision",
    "output_emitted",
    "run_completed",
    "signoff_recorded",
)


def check_audit_trail(events: list[Any]) -> list[str]:
    """Check one run's audit trail (empty list = OK).

    Per the taxonomy, every run must log all AU-01..AU-09 event types. Some runs
    cannot log every type, so the trail is checked against what the run itself
    reports:

    - Tool calls: run_completed (AU-08) records tool_call_count from the policy
      layer. The number of tool_call (AU-02) and policy_decision (AU-06) events
      must equal it. A count of zero is the only way those events may be absent,
      so a dropped event is caught rather than mistaken for "no calls".
    - Barriers, tasks, approvals: judged against the plan in output_emitted (AU-07).
    - Sign-offs (AU-09): one per gated action in that plan, logged after it.
    """
    errors: list[str] = []
    if not events:
        return ["audit trail is empty"]

    if len({e.run_id for e in events}) != 1 or len({e.case_id for e in events}) != 1:
        errors.append("events from more than one run or case")
    if [e.sequence for e in events] != list(range(len(events))):
        errors.append("sequence numbers must run 0..n-1 in log order")
    if any(b.timestamp < a.timestamp for a, b in zip(events, events[1:])):
        errors.append("timestamps go backwards")
    if events[0].event_type != "case_loaded":
        errors.append("first event must be case_loaded (AU-01)")
    if events[-1].event_type != "run_completed":
        errors.append("last event must be run_completed (AU-08)")

    present = {e.event_type for e in events}
    optional = set()
    completed = [e for e in events if e.event_type == "run_completed"]
    if len(completed) > 1:
        errors.append("run_completed (AU-08) logged more than once")
    reported_calls = completed[-1].details.tool_call_count if completed else None
    if reported_calls == 0:
        optional |= {"tool_call", "policy_decision"}
    outputs = [e for e in events if e.event_type == "output_emitted"]
    if len(outputs) > 1:
        errors.append("output_emitted (AU-07) logged more than once")
    plan = outputs[0].details.plan if outputs else None
    if plan is not None:
        if not plan.barriers:
            optional.add("barrier_flagged")
        if not plan.tasks:
            optional.add("task_recommended")
        if not plan.actions:
            optional.add("approval_classification")
        if not gated_actions(plan):
            optional.add("signoff_recorded")
    else:
        optional.add("signoff_recorded")
    for t in REQUIRED_EVENT_TYPES:
        if t not in present and t not in optional:
            errors.append(f"missing {t} event")

    by_type: dict[str, list] = {}
    for e in events:
        by_type.setdefault(e.event_type, []).append(e.details)

    call_events = by_type.get("tool_call", [])
    decision_events = by_type.get("policy_decision", [])
    if reported_calls is not None:
        for name, logged in (("tool_call", call_events), ("policy_decision", decision_events)):
            if len(logged) != reported_calls:
                errors.append(
                    f"run_completed reports {reported_calls} tool calls but {len(logged)} {name} events were logged"
                )
    calls = [d.call.call_id for d in call_events]
    if len(calls) != len(set(calls)):
        errors.append("the same tool call was logged more than once")
    calls = set(calls)
    decided = {d.call_id for d in decision_events}
    if calls != decided:
        errors.append(f"tool calls without a policy decision or vice versa: {sorted(calls ^ decided)}")

    if plan is not None:
        logged_b = {d.barrier_id for d in by_type.get("barrier_flagged", [])}
        planned_b = {b.barrier_id for b in plan.barriers}
        if logged_b != planned_b:
            errors.append(f"barrier_flagged events {sorted(logged_b)} != plan barriers {sorted(planned_b)}")
        logged_t = {d.task_id for d in by_type.get("task_recommended", [])}
        planned_t = {t.task_id for t in plan.tasks}
        if logged_t != planned_t:
            errors.append(f"task_recommended events {sorted(logged_t)} != plan tasks {sorted(planned_t)}")
        logged_a = {d.recommendation_id for d in by_type.get("approval_classification", [])}
        planned_a = {a.recommendation.recommendation_id for a in plan.actions}
        if logged_a != planned_a:
            errors.append(f"approval events {sorted(logged_a)} != plan actions {sorted(planned_a)}")
        denied = {d.call_id for d in by_type.get("policy_decision", []) if d.decision == "denied"}
        if denied != {d.call_id for d in plan.denied_tool_calls}:
            errors.append("denied policy decisions do not match plan.denied_tool_calls")
        signed = [d.recommendation_id for d in by_type.get("signoff_recorded", [])]
        gated = {a.recommendation.recommendation_id for a in gated_actions(plan)}
        if len(signed) != len(set(signed)) or set(signed) != gated:
            errors.append(f"signoff_recorded events {sorted(signed)} != gated plan actions {sorted(gated)}")
        emitted_at = events.index(outputs[0])
        if any(e.event_type == "signoff_recorded" and i < emitted_at for i, e in enumerate(events)):
            errors.append("signoff_recorded logged before output_emitted; sign-off reviews the composed plan")
    elif "signoff_recorded" in by_type:
        errors.append("signoff_recorded logged with no output_emitted plan")
    return errors
