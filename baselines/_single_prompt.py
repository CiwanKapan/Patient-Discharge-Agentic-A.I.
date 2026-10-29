"""B2's one model call, with the same format retry as the pipeline.

A response that does not parse against ``SinglePromptOutput`` is a format
failure. It is retried with the same follow-up prompt the pipeline uses
(``retry_prompt``), up to ``max_attempts`` attempts. This is the only retry B2
gets: it has no taxonomy or evidence validation, so the pipeline's validation
retries have nothing to correspond to here.

Two ways to make the call, with identical retry behavior:

    ask        one case at a time, through ``llm.complete``
    ask_batch  many cases through the Batch API (50% price); attempt k of every
               case that needs it goes out as batch k
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pydantic import BaseModel, ValidationError

from src.pipeline._common import format_errors
from src.utils.llm import LLMError, LLMInfraError, call_record, retry_prompt


@dataclass
class Answer:
    out: Optional[BaseModel] = None
    raw: Optional[str] = None
    calls: list = field(default_factory=list)  # LLMCallRecord per attempt
    error: Optional[str] = None
    error_kind: Optional[str] = None  # "infrastructure" or "output"


def _parse(schema, raw):
    try:
        return schema.model_validate_json(raw), []
    except ValidationError as e:
        return None, format_errors(e)


def _fail(answer: Answer, e: LLMError) -> Answer:
    answer.error = str(e)
    answer.error_kind = "infrastructure" if isinstance(e, LLMInfraError) else "output"
    return answer


def ask(llm, step: str, system: str, user: str, schema: type[BaseModel], max_attempts: int) -> Answer:
    answer, prompt = Answer(), user
    for attempt in range(1, max_attempts + 1):
        try:
            raw = llm.complete(step, system, prompt, schema)
        except LLMError as e:
            answer.calls.append(call_record(llm, step, attempt, "llm_error", [str(e)]))
            return _fail(answer, e)
        answer.raw = raw
        out, errors = _parse(schema, raw)
        if out is not None:
            answer.calls.append(call_record(llm, step, attempt, "accepted"))
            answer.out = out
            return answer
        answer.calls.append(call_record(llm, step, attempt, "format_error", errors))
        prompt = retry_prompt(user, raw, errors)
    answer.error = f"unparseable output after {max_attempts} attempts: {answer.calls[-1].errors[0]}"
    answer.error_kind = "output"
    return answer


def ask_batch(llm, step: str, prompts: dict[str, tuple[str, str]], schema: type[BaseModel], max_attempts: int,
              **batch_kw) -> dict[str, Answer]:
    """``prompts`` maps a custom_id to (system, user). Returns an Answer per custom_id."""
    answers = {cid: Answer() for cid in prompts}
    pending = {cid: user for cid, (_, user) in prompts.items()}
    for attempt in range(1, max_attempts + 1):
        if not pending:
            break
        requests = {cid: llm.params(prompts[cid][0], user, schema) for cid, user in pending.items()}
        results = llm.run_batch(requests, **batch_kw)
        retry = {}
        for cid, res in results.items():
            a = answers[cid]
            if res["error"] is not None:
                a.calls.append(call_record(llm, step, attempt, "llm_error", [str(res["error"])], usage=res["usage"] or {}))
                _fail(a, res["error"])
                continue
            a.raw = res["text"]
            out, errors = _parse(schema, res["text"])
            if out is not None:
                a.calls.append(call_record(llm, step, attempt, "accepted", usage=res["usage"]))
                a.out = out
            else:
                a.calls.append(call_record(llm, step, attempt, "format_error", errors, usage=res["usage"]))
                retry[cid] = retry_prompt(prompts[cid][1], res["text"], errors)
        pending = retry
    for cid in pending:
        a = answers[cid]
        a.error = f"unparseable output after {max_attempts} attempts: {a.calls[-1].errors[0]}"
        a.error_kind = "output"
    return answers
