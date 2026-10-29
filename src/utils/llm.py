"""LLM client used by the reasoning stages (02-05) and the single-prompt baseline (B2).

Stages depend on the small ``LLMClient`` protocol, not on the Anthropic SDK, so
tests can run the whole pipeline offline with a scripted client. The client
returns raw JSON text; the caller validates it against its Pydantic model and
rejects (never repairs) anything that does not fit.

Every call's token usage is left on ``last_usage`` so callers can log it per
call (see ``LLMCallRecord``). Errors are split by what a rerun can fix:

    LLMInfraError   the request did not complete (rate limit, server or connection
                    error, an errored or expired batch request); resuming reruns it
    LLMOutputError  the model answered but the answer is unusable (refusal,
                    truncation at max_tokens, no text); this is a result, kept as is
"""
from __future__ import annotations

import time
from typing import Callable, Optional, Protocol

from pydantic import BaseModel

from src.models.messages import Stage
from src.utils.run_config import LLMSettings

DEFAULT_MODEL = "claude-sonnet-5-5"


class LLMError(RuntimeError):
    """The model call itself failed."""


class LLMInfraError(LLMError):
    """The request did not complete; rerunning may succeed."""


class LLMOutputError(LLMError):
    """The model responded, but with nothing usable (refusal, truncation, no text)."""


class LLMClient(Protocol):
    model: str

    def complete(self, stage: Stage | str, system: str, user: str, schema: type[BaseModel]) -> str:
        """Return the model's JSON response text for ``schema``. ``stage`` labels the call."""
        ...


def usage_of(response, batch: bool = False) -> dict:
    u = response.usage
    return {
        "input_tokens": u.input_tokens,
        "output_tokens": u.output_tokens,
        "cache_read_input_tokens": getattr(u, "cache_read_input_tokens", None) or 0,
        "cache_creation_input_tokens": getattr(u, "cache_creation_input_tokens", None) or 0,
        "stop_reason": response.stop_reason,
        "request_id": getattr(response, "_request_id", None) or getattr(response, "id", None),
        "batch": batch,
    }


def text_of(response, label: str, max_tokens: int) -> str:
    """The response text, or LLMOutputError for a refusal, truncation, or missing text."""
    if response.stop_reason == "refusal":
        raise LLMOutputError(f"{label}: model refused (request {getattr(response, '_request_id', None)})")
    if response.stop_reason == "max_tokens":
        raise LLMOutputError(f"{label}: output truncated at max_tokens={max_tokens}")
    text = next((b.text for b in response.content if b.type == "text"), None)
    if text is None:
        raise LLMOutputError(f"{label}: response had no text block")
    return text


def call_record(llm, step: str, attempt: int, outcome: str, errors=(), usage: Optional[dict] = None):
    """An ``LLMCallRecord`` for the call ``llm`` just made (or for ``usage``, from a batch result)."""
    from src.models.audit import LLMCallRecord

    u = usage if usage is not None else (getattr(llm, "last_usage", None) or {})
    return LLMCallRecord(
        step=step, attempt=attempt, outcome=outcome, errors=list(errors)[:10],
        input_tokens=u.get("input_tokens"), output_tokens=u.get("output_tokens"),
        cache_read_input_tokens=u.get("cache_read_input_tokens"),
        cache_creation_input_tokens=u.get("cache_creation_input_tokens"),
        stop_reason=u.get("stop_reason"), request_id=u.get("request_id"), batch=bool(u.get("batch")),
    )


def retry_prompt(user: str, raw: str, errors: list[str]) -> str:
    """The follow-up prompt after a rejected response. Shared by every arm that retries."""
    return (
        f"{user}\n\n## Your previous response was rejected\n\n{raw}\n\n"
        "Problems found:\n" + "\n".join(f"- {e}" for e in errors) +
        "\n\nReturn a corrected response that fixes every problem."
    )


class AnthropicLLM:
    """Claude via the Anthropic SDK, with structured outputs constrained to ``schema``."""

    def __init__(
        self,
        model: str | None = None,
        effort: str = "medium",
        max_tokens: int = 16000,
        client=None,
    ):
        import anthropic

        self._anthropic = anthropic
        self._client = client or anthropic.Anthropic()
        self.model = model or DEFAULT_MODEL
        self.effort = effort
        self.max_tokens = max_tokens
        self._schemas: dict[type[BaseModel], dict] = {}
        self.last_usage: Optional[dict] = None

    @classmethod
    def from_settings(cls, settings: LLMSettings, client=None) -> "AnthropicLLM":
        return cls(model=settings.model, effort=settings.effort, max_tokens=settings.max_tokens, client=client)

    def _schema(self, schema: type[BaseModel]) -> dict:
        if schema not in self._schemas:
            self._schemas[schema] = self._anthropic.transform_schema(schema)
        return self._schemas[schema]

    def params(self, system: str, user: str, schema: type[BaseModel]) -> dict:
        """The Messages API request body, shared by direct calls and the Batch API."""
        return {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "system": [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
            "messages": [{"role": "user", "content": user}],
            "output_config": {
                "effort": self.effort,
                "format": {"type": "json_schema", "schema": self._schema(schema)},
            },
        }

    def complete(self, stage: Stage | str, system: str, user: str, schema: type[BaseModel]) -> str:
        anthropic = self._anthropic
        label = getattr(stage, "value", stage)
        self.last_usage = None
        try:
            response = self._client.messages.create(**self.params(system, user, schema))
        except anthropic.APIStatusError as e:
            kind = LLMInfraError if e.status_code == 429 or e.status_code >= 500 else LLMError
            raise kind(f"{label}: API error {e.status_code}: {e.message}") from e
        except anthropic.APIConnectionError as e:
            raise LLMInfraError(f"{label}: connection error: {e}") from e
        self.last_usage = usage_of(response)
        return text_of(response, label, self.max_tokens)

    # ---------------------------------------------------------------- Batch API
    def run_batch(self, requests: dict[str, dict], poll_seconds: float = 30.0,
                  on_poll: Optional[Callable[[object], None]] = None) -> dict[str, dict]:
        """Submit ``{custom_id: params}`` as one batch (50% price) and wait for it.

        Returns ``{custom_id: {"text": str | None, "usage": dict | None, "error": LLMError | None}}``.
        Results arrive in any order and are keyed by custom_id.
        """
        if not requests:
            return {}
        batch = self._client.messages.batches.create(
            requests=[{"custom_id": cid, "params": p} for cid, p in requests.items()])
        while True:
            batch = self._client.messages.batches.retrieve(batch.id)
            if on_poll:
                on_poll(batch)
            if batch.processing_status == "ended":
                break
            time.sleep(poll_seconds)
        out: dict[str, dict] = {}
        for r in self._client.messages.batches.results(batch.id):
            kind = r.result.type
            if kind == "succeeded":
                msg = r.result.message
                usage = usage_of(msg, batch=True)
                try:
                    out[r.custom_id] = {"text": text_of(msg, r.custom_id, self.max_tokens), "usage": usage, "error": None}
                except LLMOutputError as e:
                    out[r.custom_id] = {"text": None, "usage": usage, "error": e}
            elif kind == "errored" and getattr(r.result.error, "type", "") == "invalid_request":
                out[r.custom_id] = {"text": None, "usage": None,
                                    "error": LLMError(f"{r.custom_id}: invalid batch request: {r.result.error}")}
            else:
                out[r.custom_id] = {"text": None, "usage": None,
                                    "error": LLMInfraError(f"{r.custom_id}: batch request {kind}")}
        for cid in requests.keys() - out.keys():
            out[cid] = {"text": None, "usage": None, "error": LLMInfraError(f"{cid}: no batch result")}
        return out
