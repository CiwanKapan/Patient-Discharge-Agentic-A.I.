"""LLM client used by the reasoning stages (02-05) and Baseline 2.

Stages depend on the small ``LLMClient`` protocol, not on the Anthropic SDK, so
tests can run the whole pipeline offline with a scripted client. The client
returns raw JSON text; the calling stage validates it against its Pydantic
model and rejects (never repairs) anything that does not fit.
"""
from __future__ import annotations

import os
from typing import Protocol

from pydantic import BaseModel

from src.models.messages import Stage

DEFAULT_MODEL = "claude-sonnet-5-5"


class LLMError(RuntimeError):
    """The model call itself failed (API error, refusal, truncated output)."""


class LLMClient(Protocol):
    model: str

    def complete(self, stage: Stage | str, system: str, user: str, schema: type[BaseModel]) -> str:
        """Return the model's JSON response text for ``schema``. ``stage`` labels the call."""
        ...


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
        self.model = model or os.environ.get("CLAUDE_MODEL", DEFAULT_MODEL)
        self.effort = effort
        self.max_tokens = max_tokens
        self._schemas: dict[type[BaseModel], dict] = {}

    def _schema(self, schema: type[BaseModel]) -> dict:
        if schema not in self._schemas:
            self._schemas[schema] = self._anthropic.transform_schema(schema)
        return self._schemas[schema]

    def complete(self, stage: Stage | str, system: str, user: str, schema: type[BaseModel]) -> str:
        anthropic = self._anthropic
        label = getattr(stage, "value", stage)
        try:
            response = self._client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
                messages=[{"role": "user", "content": user}],
                output_config={
                    "effort": self.effort,
                    "format": {"type": "json_schema", "schema": self._schema(schema)},
                },
            )
        except anthropic.APIStatusError as e:
            raise LLMError(f"{label}: API error {e.status_code}: {e.message}") from e
        except anthropic.APIConnectionError as e:
            raise LLMError(f"{label}: connection error: {e}") from e

        if response.stop_reason == "refusal":
            raise LLMError(f"{label}: model refused (request {response._request_id})")
        if response.stop_reason == "max_tokens":
            raise LLMError(f"{label}: output truncated at max_tokens={self.max_tokens}")
        text = next((b.text for b in response.content if b.type == "text"), None)
        if text is None:
            raise LLMError(f"{label}: response had no text block")
        return text
