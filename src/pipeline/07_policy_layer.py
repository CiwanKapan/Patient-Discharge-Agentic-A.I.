"""Stage 07 - Policy Layer (deterministic).

Every tool call passes through here before anything runs. Default deny: a tool
runs only if it is on the taxonomy's allowed list (GA-T*). Forbidden tools
(GF-T*) and tools on neither list are denied and never executed. Allowed tools
run against the mock implementations in src/tools/allowed_tools.py.
"""
from __future__ import annotations

from src.models.case import PatientCase
from src.models.messages import AgentMessage, Stage
from src.models.plan import RecommendationSet
from src.models.tools import PolicyDecision, PolicyLayerOutput, ToolCall, ToolResult
from src.pipeline._common import RunContext, make_message
from src.tools.allowed_tools import ALLOWED_TOOLS

STAGE = Stage.POLICY_LAYER


def decide(taxonomy: dict, call: ToolCall) -> PolicyDecision:
    gov = taxonomy["governance"]
    allowed = {t["tool_name"]: t for t in gov["allowed_tools"]}
    forbidden = {t["tool_name"]: t for t in gov["forbidden_tools"]}
    base = dict(call_id=call.call_id, tool_name=call.tool_name)
    if call.tool_name in allowed:
        rule = allowed[call.tool_name]
        return PolicyDecision(**base, decision="allowed", rule_id=rule["id"], reason=f"On the allowed list ({rule['side_effect']}).")
    if call.tool_name in forbidden:
        rule = forbidden[call.tool_name]
        return PolicyDecision(**base, decision="denied", rule_id=rule["id"], reason=f"Forbidden tool: {rule['reason']}")
    return PolicyDecision(**base, decision="denied", reason="Not on the allowed list (default deny).")


def execute(case: PatientCase, call: ToolCall) -> ToolResult:
    tool = ALLOWED_TOOLS.get(call.tool_name)
    if tool is None:
        return ToolResult(call_id=call.call_id, error=f"{call.tool_name} is allowed but has no implementation")
    try:
        return ToolResult(call_id=call.call_id, output=tool(case, call.arguments))
    except Exception as e:  # a failing mock tool must not take the run down with it
        return ToolResult(call_id=call.call_id, error=f"{type(e).__name__}: {e}")


def review(ctx: RunContext, calls: list[ToolCall]) -> PolicyLayerOutput:
    decisions, results = [], []
    for call in calls:
        d = decide(ctx.taxonomy, call)
        decisions.append(d)
        if d.decision == "allowed":
            results.append(execute(ctx.case, call))
    return PolicyLayerOutput(decisions=decisions, results=results)


def proposed_calls(recs: RecommendationSet) -> list[ToolCall]:
    return [c for r in recs.recommendations for c in r.proposed_tool_calls]


def run(ctx: RunContext, recs: AgentMessage[RecommendationSet], approvals: AgentMessage) -> AgentMessage[PolicyLayerOutput]:
    payload = review(ctx, proposed_calls(recs.payload))
    return make_message(ctx, STAGE, payload, [recs, approvals])
