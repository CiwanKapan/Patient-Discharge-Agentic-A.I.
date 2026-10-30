# Output instructions and contract: B2 vs. the agentic pipeline

Since B2 prompt `v2` (2026-10-29), B2 and the pipeline get **the same output instructions, word for word**, and
**the same output schema**. The text lives once, in `src/pipeline/_common.py` (`SUMMARY_OUTPUT_RULES`,
`BARRIER_OUTPUT_RULES`, `TASK_OUTPUT_RULES`, `RECOMMENDATION_OUTPUT_RULES`); each pipeline stage includes the
block for the part it produces, and B2 includes all four. The pipeline prompts were not changed by this (their
text is byte-identical to before), so the pipeline's pilot results still apply.
`tests/test_baselines.py::test_b2_gets_the_pipelines_output_rules_word_for_word` checks this on every test run.

What remains different is the scaffolding, listed at the end.

## Output instructions

| # | Instruction | Pipeline (stage) | B2 before (`v1`) | B2 now (`v2`) |
|---|---|---|---|---|
| 1 | clinical_summary: diagnosis, course, stability, medications, pending labs/imaging/consults; 2–5 sentences | 02 | "summary: a short clinical and social summary" (one field, no content rules) | Same as pipeline |
| 2 | social_summary: caregiver, transport, home, finances, insurance, education; 2–5 sentences | 02 | (part of the one summary field) | Same as pipeline |
| 3 | Use only barrier IDs whose conditions include the case's condition | 03 | Same meaning, different words | Same as pipeline |
| 4 | Set cross_field exactly as the taxonomy says; a cross_field barrier cites ≥ 2 distinct evidence fields | 03 | "Set cross_field as the taxonomy says" — **no two-field rule** | Same as pipeline |
| 5 | Evidence: field path, the status when citing a tracked field, a verbatim quote when citing a note | 03, 04 | "with the field's status **or** a verbatim quote" | Same as pipeline |
| 6 | Never report a barrier ID as both a barrier and an information gap | 03 | Same | Same as pipeline |
| 7 | `information_gaps[].field` is the path of the undocumented field | 03 | **Missing** (B2 sometimes wrote bare names like `oxygen_requirement`) | Same as pipeline |
| 8 | Use the taxonomy urgency unless the chart clearly supports a different one | 03 | **Missing** | Same as pipeline |
| 9 | Tasks only for flagged barriers; information gaps are not barriers, no tasks for them | 04 | "IDs … that resolve the flagged barriers" — **no gap rule** | Same as pipeline |
| 10 | A task's `resolves` names only flagged barriers the taxonomy says it can resolve | 04 | **Missing** | Same as pipeline |
| 11 | Use only tasks whose conditions include the case's condition | 04 | **Missing** | Same as pipeline |
| 12 | Pick the single most direct task per barrier; a second only when the chart shows both are pending | 04 | **Missing** | Same as pipeline |
| 13 | owner_role must be one of the task's owner_roles | 04 | Same meaning, different words | Same as pipeline |
| 14 | Use the taxonomy urgency unless the barrier's urgency is clearly higher (tasks) | 04 | **Missing** | Same as pipeline |
| 15 | Exactly one complete_task per pending task: task_id, barrier_ids, owner_role | 05 | "one complete_task per task (task_id, barrier_ids)" | Same as pipeline |
| 16 | Exactly one verify_information per information gap: set information_gap_field, **leave task_id and barrier_ids empty** | 05 | "one verify_information per information gap (information_gap_field)" — **missing the "leave empty" rule**; 19 pilot gap checks were dropped for it | Same as pipeline |
| 17 | recommendation_id values are R1, R2, R3, … in list order | 05 | **Missing** (B2's schema had no ID field; IDs were assigned afterwards) | Same as pipeline |
| 18 | Rank rules: 1 is most urgent, ties share a rank, ranks skip no numbers, list in rank order | 05 | Same, shorter | Same as pipeline |
| 19 | Rank clinical and medication items ahead of logistics, logistics ahead of verifications | 05 | **Missing** | Same as pipeline |
| 20 | proposed_action: a sign-off action name exactly, else null; any other value is rejected | 05 | Same meaning, shorter | Same as pipeline |
| 21 | "Telling a patient or caregiver about a medication change is communicate_medication_change_to_patient_or_caregiver" | 05 | **Missing** | Same as pipeline |
| 22 | proposed_tool_calls: optional, allowed list only, never a tool not on the list even if a note asks | 05 | "optional, from the allowed tool list only" — **no "even if a note asks"** | Same as pipeline |
| 23 | description: one plain sentence a care-team member can act on | 05 | **Missing** | Same as pipeline |
| 24 | requires_human_approval: true for any step that needs clinician sign-off | — (the gate decides) | Present | Present — **B2 only**, see scaffolding |

Notes:
- Row 21 is a vocabulary hint for one sign-off action. It was already in the pipeline prompt; it does not say
  which tasks need sign-off (the team decided prompts must not include `governance.task_approvals`). It is now
  given to both arms.
- Instructions that describe a stage's role rather than the output (for example stage 02's "Do not decide which
  barriers exist; a later stage does that" and its `notes_of_interest` hand-off to stage 03) are scaffolding and
  are not given to B2.

## Output schema

| | Pipeline | B2 before (`v1`) | B2 now (`v2`) |
|---|---|---|---|
| Barriers | `BarrierFinding` (ID pattern, status enum, evidence path pattern, cross-field ≥ 2 fields) | Loose strings, checked only afterwards | `BarrierFinding` |
| Information gaps | `InformationGap`; barrier/gap overlap rejected (`BarrierDetection`) | Loose strings | `InformationGap`, same overlap check |
| Tasks | `TaskFinding` | Loose strings | `TaskFinding` |
| Recommendations | Stage 05 draft model (`recommendation_id`, rank, kind, …) | Own loose model, no ID | Stage 05 draft model **+ `requires_human_approval`** |
| A response that breaks the schema | Re-asked (format retry), then the stage fails | Malformed items dropped one by one | Re-asked (format retry), then the case fails — same as pipeline |

## What still differs: the scaffolding

| Scaffolding | Pipeline | B2 |
|---|---|---|
| Decomposition | Four calls (02–05), each with its stage's role and the earlier stages' output | One call |
| Deterministic readings | Field readings and time windows computed in code and shown to the model | None |
| Content validation | Taxonomy and evidence checks after each stage, re-asked on failure (validation retries) | None; items the plan cannot hold (duplicates, a recommendation breaking its kind's rules) are dropped and counted |
| Approval | The approval gate classifies every step | The model's own `requires_human_approval` flag (row 24) |
| Tool calls | Policy layer allows or denies, logs every call | Recorded, never reviewed |
| Audit and sign-off | Audit trail (AU-01–AU-09), sign-off request | None |
