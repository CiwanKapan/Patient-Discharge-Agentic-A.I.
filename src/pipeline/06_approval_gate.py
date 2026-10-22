"""Stage 06 - Approval Gate (deterministic).

Tags every recommendation with exactly one safety classification:

    forbidden                 it would call a forbidden tool (GF-T*), or its
                              proposed action is a forbidden tool and not an
                              approval-required action
    requires_human_approval   its proposed action is approval-required (GR-A*)
    auto_safe                 nothing it proposes is approval-required or forbidden

Some names are both a GR-A* action and a GF-T* tool (e.g. modify_medication_list).
Proposing the action for a clinician needs approval; calling the tool is forbidden.
This mirrors ``check_governance`` in src/models/plan.py, which verifies the result.
"""
from __future__ import annotations

from src.models.messages import AgentMessage, Stage
from src.models.plan import ApprovalClassification, ApprovalDecisions, Recommendation, RecommendationSet
from src.pipeline._common import RunContext, make_message

STAGE = Stage.APPROVAL_GATE


def classify(taxonomy: dict, rec: Recommendation) -> ApprovalClassification:
    gov = taxonomy["governance"]
    gr = {a["action"]: a for a in gov["approval_required_actions"]}
    gf = {t["tool_name"]: t for t in gov["forbidden_tools"]}

    forbidden = [gf[c.tool_name] for c in rec.proposed_tool_calls if c.tool_name in gf]
    if rec.proposed_action in gf and rec.proposed_action not in gr:
        forbidden.append(gf[rec.proposed_action])
    if forbidden:
        hit = min(forbidden, key=lambda t: t["id"])
        names = ", ".join(sorted({t["tool_name"] for t in forbidden}))
        return ApprovalClassification(
            recommendation_id=rec.recommendation_id,
            classification="forbidden",
            requires_human_approval=False,
            matched_rule_id=hit["id"],
            reason=f"Proposes forbidden tool(s) {names}: {hit['reason']}",
        )
    if rec.proposed_action in gr:
        rule = gr[rec.proposed_action]
        return ApprovalClassification(
            recommendation_id=rec.recommendation_id,
            classification="requires_human_approval",
            requires_human_approval=True,
            matched_rule_id=rule["id"],
            reason=f"{rec.proposed_action} requires clinician approval: {rule['reason']}",
        )
    return ApprovalClassification(
        recommendation_id=rec.recommendation_id,
        classification="auto_safe",
        requires_human_approval=False,
        reason="No approval-required action or forbidden tool proposed.",
    )


def run(ctx: RunContext, recs: AgentMessage[RecommendationSet]) -> AgentMessage[ApprovalDecisions]:
    payload = ApprovalDecisions(classifications=[classify(ctx.taxonomy, r) for r in recs.payload.recommendations])
    return make_message(ctx, STAGE, payload, [recs])
