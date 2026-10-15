"""Tool calls and policy-layer decisions (stage 07).

Default deny: a tool is allowed only if it is on the taxonomy's allowed list
(GA-T*). Forbidden tools (GF-T*) and tools on neither list are denied, and
every denial is logged (audit event AU-06).
"""
from __future__ import annotations

import uuid
from typing import Any, ClassVar, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from src.models.messages import AgentMessage, Stage

class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ToolCall(_Strict):
    """A request to run a tool. Proposed by an LLM stage, never run before policy review."""

    call_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    tool_name: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    arguments: dict[str, Any] = Field(default_factory=dict)
    requested_by: Stage


class ToolResult(_Strict):
    """What an allowed tool returned. Mock tools only; no real EHR access."""

    call_id: str
    output: Optional[dict[str, Any]] = None
    error: Optional[str] = None

    @model_validator(mode="after")
    def _output_or_error(self) -> "ToolResult":
        if (self.output is None) == (self.error is None):
            raise ValueError("a tool result has exactly one of output or error")
        return self


class PolicyDecision(_Strict):
    call_id: str
    tool_name: str
    decision: Literal["allowed", "denied"]
    rule_id: Optional[str] = Field(
        None,
        pattern=r"^G[AF]-T\d{2}$",
        description="Matching GA-T*/GF-T* entry, or null for a tool on neither list.",
    )
    reason: str

    @model_validator(mode="after")
    def _consistent(self) -> "PolicyDecision":
        if self.decision == "allowed" and not (self.rule_id or "").startswith("GA-T"):
            raise ValueError("only tools on the allowed list (GA-T*) may be allowed")
        if (self.rule_id or "").startswith("GF-T") and self.decision != "denied":
            raise ValueError("forbidden tools (GF-T*) must be denied")
        return self


class PolicyLayerOutput(_Strict):
    STAGE: ClassVar[Stage] = Stage.POLICY_LAYER

    decisions: list[PolicyDecision] = Field(default_factory=list)
    results: list[ToolResult] = Field(default_factory=list, description="Results of allowed calls only.")

    @model_validator(mode="after")
    def _results_only_for_allowed(self) -> "PolicyLayerOutput":
        ids = [d.call_id for d in self.decisions]
        if len(ids) != len(set(ids)):
            raise ValueError("each tool call gets exactly one policy decision")
        allowed = {d.call_id for d in self.decisions if d.decision == "allowed"}
        stray = [r.call_id for r in self.results if r.call_id not in allowed]
        if stray:
            raise ValueError(f"results present for calls that were not allowed: {stray}")
        return self


def check_policy(taxonomy: dict, output: PolicyLayerOutput) -> list[str]:
    """Confirm each decision matches the taxonomy's tool lists (empty list = OK)."""
    gov = taxonomy["governance"]
    allowed = {t["tool_name"]: t["id"] for t in gov["allowed_tools"]}
    forbidden = {t["tool_name"]: t["id"] for t in gov["forbidden_tools"]}
    errors = []
    for d in output.decisions:
        if d.tool_name in allowed:
            want = ("allowed", allowed[d.tool_name])
        elif d.tool_name in forbidden:
            want = ("denied", forbidden[d.tool_name])
        else:
            want = ("denied", None)
        if (d.decision, d.rule_id) != want:
            errors.append(f"{d.tool_name}: got {d.decision}/{d.rule_id}, expected {want[0]}/{want[1]}")
    return errors


PolicyLayerMessage = AgentMessage[PolicyLayerOutput]
