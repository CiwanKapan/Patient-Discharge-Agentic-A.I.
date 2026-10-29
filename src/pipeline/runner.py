"""Runs one case through stages 01-09 and writes its audit trail.

    01 read -> 02 analyze -> 03 barriers -> 04 tasks -> 05 recommend
            -> 06 approval gate -> 07 policy layer -> 08 compose -> 09 sign-off

Each stage's output is logged as it is produced (AU-01..AU-07, then AU-09 for
each sign-off decision), and the run always ends with run_completed (AU-08),
including when a stage fails. A failed stage stops the run; nothing downstream
sees its output. ``RunResult.plan`` is the composed plan (what the system
produced); ``RunResult.signoffs`` holds the reviewer's decision on each gated action.
"""
from __future__ import annotations

import importlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from src.models.audit import (
    ApprovalClassificationDetails,
    ApprovalClassified,
    BarrierFlagged,
    BarrierFlaggedDetails,
    CaseLoaded,
    OutputEmitted,
    OutputEmittedDetails,
    PolicyDecisionDetails,
    PolicyDecisionEvent,
    RunCompleted,
    RunCompletedDetails,
    SignoffRecorded,
    TaskRecommended,
    TaskRecommendedDetails,
    ToolCallDetails,
    ToolCallEvent,
    check_audit_trail,
)
from src.models.messages import AgentMessage, Stage
from src.models.plan import DischargePlan, SignoffDecision, check_governance
from src.models.tools import check_policy
from src.pipeline._common import PROMPT_VERSION, RunContext, StageError, load_taxonomy, make_message
from src.utils.audit_logger import AuditLogger, read_audit_log
from src.utils.llm import LLMClient, LLMError, LLMInfraError

input_reader = importlib.import_module("src.pipeline.01_input_reader")
case_analyzer = importlib.import_module("src.pipeline.02_case_analyzer")
barrier_detector = importlib.import_module("src.pipeline.03_barrier_detector")
task_detector = importlib.import_module("src.pipeline.04_task_detector")
rec_generator = importlib.import_module("src.pipeline.05_rec_generator")
approval_gate = importlib.import_module("src.pipeline.06_approval_gate")
policy_layer = importlib.import_module("src.pipeline.07_policy_layer")
output_composer = importlib.import_module("src.pipeline.08_output_composer")
signoff = importlib.import_module("src.pipeline.09_signoff")

LLM_STAGES = (Stage.CASE_ANALYZER, Stage.BARRIER_DETECTOR, Stage.TASK_DETECTOR, Stage.REC_GENERATOR)
DEFAULT_AUDIT_DIR = Path("runs") / "audit"


@dataclass
class RunResult:
    run_id: str
    case_id: str
    status: str
    audit_path: Path
    plan: Optional[DischargePlan] = None
    signoffs: list[SignoffDecision] = field(default_factory=list)
    messages: list[AgentMessage] = field(default_factory=list)
    error: Optional[str] = None
    error_kind: Optional[str] = None  # "infrastructure" (a rerun may succeed) or "output" (a result)
    audit_errors: list[str] = field(default_factory=list)
    llm_calls: list = field(default_factory=list)  # LLMCallRecord per model call


def run_case(
    case_path: str | Path,
    llm: LLMClient,
    *,
    taxonomy: Optional[dict] = None,
    audit_dir: str | Path = DEFAULT_AUDIT_DIR,
    run_id: Optional[str] = None,
    max_attempts: int = 2,
    reviewer: Optional[signoff.Reviewer] = None,
    llm_settings: Optional[dict] = None,
) -> RunResult:
    """Run one case. ``reviewer`` decides sign-off in stage 09; the default leaves every gated action pending.
    ``llm_settings`` (from config/run_config.json) is recorded in run_completed."""
    taxonomy = taxonomy or load_taxonomy()
    reviewer = reviewer or signoff.PendingReviewer()
    run_id = run_id or uuid.uuid4().hex
    started = datetime.now(timezone.utc)
    loaded = input_reader.read_case(case_path)
    result = RunResult(run_id, loaded.case_id, "failed", Path(audit_dir) / loaded.case_id / f"{run_id}.jsonl")
    tool_call_count = 0

    with AuditLogger(result.audit_path, run_id, loaded.case_id) as log:
        log.log(CaseLoaded, loaded.details, stage=Stage.INPUT_READER)
        try:
            if loaded.case is None:
                raise StageError(Stage.INPUT_READER, loaded.error)
            ctx = RunContext(run_id, loaded.case, taxonomy, llm, max_attempts, llm_calls=result.llm_calls)
            msgs = result.messages

            m_case = make_message(ctx, Stage.INPUT_READER, loaded.case)
            msgs.append(m_case)

            m_summary = case_analyzer.run(ctx, m_case)
            msgs.append(m_summary)

            m_barriers = barrier_detector.run(ctx, m_summary)
            msgs.append(m_barriers)
            for b in m_barriers.payload.barriers:
                details = BarrierFlaggedDetails(
                    barrier_id=b.barrier_id,
                    evidence_fields=list(dict.fromkeys(e.field for e in b.evidence)),
                    urgency=b.urgency,
                )
                log.log(BarrierFlagged, details, Stage.BARRIER_DETECTOR, m_barriers.message_id)

            m_tasks = task_detector.run(ctx, m_summary, m_barriers)
            msgs.append(m_tasks)
            for t in m_tasks.payload.tasks:
                details = TaskRecommendedDetails(task_id=t.task_id, owner_role=t.owner_role, linked_barrier_ids=t.resolves)
                log.log(TaskRecommended, details, Stage.TASK_DETECTOR, m_tasks.message_id)

            m_recs = rec_generator.run(ctx, m_barriers, m_tasks)
            msgs.append(m_recs)

            m_approvals = approval_gate.run(ctx, m_recs)
            msgs.append(m_approvals)
            for c in m_approvals.payload.classifications:
                log.log(ApprovalClassified, ApprovalClassificationDetails(**c.model_dump()),
                        Stage.APPROVAL_GATE, m_approvals.message_id)
            errors = check_governance(taxonomy, m_recs.payload, m_approvals.payload)
            if errors:
                raise StageError(Stage.APPROVAL_GATE, "governance check failed: " + "; ".join(errors))

            m_policy = policy_layer.run(ctx, m_recs, m_approvals)
            msgs.append(m_policy)
            calls = {c.call_id: c for c in policy_layer.proposed_calls(m_recs.payload)}
            results = {r.call_id: r for r in m_policy.payload.results}
            for d in m_policy.payload.decisions:
                r = results.get(d.call_id)
                log.log(ToolCallEvent, ToolCallDetails(
                    call=calls[d.call_id], decision=d.decision,
                    output=r.output if r else None, error=r.error if r else None,
                ), Stage.POLICY_LAYER, m_policy.message_id)
                log.log(PolicyDecisionEvent, PolicyDecisionDetails(**d.model_dump()), Stage.POLICY_LAYER, m_policy.message_id)
                tool_call_count += 1
            errors = check_policy(taxonomy, m_policy.payload)
            if errors:
                raise StageError(Stage.POLICY_LAYER, "policy check failed: " + "; ".join(errors))

            m_plan = output_composer.run(ctx, m_summary, m_barriers, m_tasks, m_recs, m_approvals, m_policy)
            msgs.append(m_plan)
            log.log(OutputEmitted, OutputEmittedDetails(plan=m_plan.payload), Stage.OUTPUT_COMPOSER, m_plan.message_id)

            m_signoff = signoff.run(ctx, m_plan, reviewer)
            msgs.append(m_signoff)
            for d in m_signoff.payload.decisions:
                log.log(SignoffRecorded, d, Stage.SIGNOFF, m_signoff.message_id)
            result.plan = m_plan.payload
            result.signoffs = m_signoff.payload.decisions
            result.status = "succeeded"
        except (StageError, LLMError) as e:
            result.error = str(e)
            result.error_kind = "infrastructure" if isinstance(e, LLMInfraError) else "output"
        except Exception as e:  # a bug, not a model failure: log the failed run, then surface it
            result.error = f"{type(e).__name__}: {e}"
            result.error_kind = "bug"
            _complete(log, result, llm, started, tool_call_count, llm_settings)
            raise
        _complete(log, result, llm, started, tool_call_count, llm_settings)

    result.audit_errors = check_audit_trail(read_audit_log(result.audit_path))
    return result


def _complete(log: AuditLogger, result: RunResult, llm: LLMClient, started: datetime, tool_call_count: int,
              llm_settings: Optional[dict] = None) -> None:
    log.log(RunCompleted, RunCompletedDetails(
        status=result.status,
        model=getattr(llm, "model", "none"),
        prompt_versions={s.value: PROMPT_VERSION for s in LLM_STAGES},
        started_at=started,
        completed_at=datetime.now(timezone.utc),
        tool_call_count=tool_call_count,
        error=result.error,
        llm_calls=result.llm_calls,
        llm_settings=llm_settings,
    ))
