# Review packet — Dataset Lead and clinical lead

**Prepared 2026-10-29, before any run on the 160 evaluation cases.** Every item below must be decided before
that run. For each: what changes, why, the evidence, how many answer keys it affects, and whether it changes
what the models are told (the prompts). **Any decision that changes the prompts means re-running the
15-case development pilot before the evaluation run** (about $3); key-only changes do not.

Counts are for the 160 evaluation keys unless noted ("dev" = the 15 development cases). Reviewer fields are at
the end of each item.

**Status (updated 2026-10-29 with the team's decisions):** decisions on items 5–11 are recorded under each item; items 5 and 7 are applied in **taxonomy 2.2**; item 8 is withdrawn (B-F02 removed in **taxonomy 2.3**, Amendment 3). Items 1–4 are already applied in taxonomy 2.1 and were approved by the
Dataset Lead on 2026-10-29; they are listed again for the clinical lead's sign-off. Items 5–11 are open.

---

## 1. T-CM09 "Assign covering case manager" — new task, owner: nurse (charge nurse)

| | |
|---|---|
| **Change** | New task resolving B-S05 (case manager unavailable). Owner: nurse only (the charge nurse requests a covering case manager); social worker removed. Urgency high; all five conditions. |
| **Why** | B-S05 had no task in taxonomy 2.0, so a correct system could never address it. The case manager cannot be the owner, being the person who is unavailable. |
| **Answer keys affected** | **16** gained T-CM09 (+1 dev). The owner choice changes **0** keys (keys do not record owners). |
| **Prompts** | Yes (already in effect; the pilot ran with it). |

Decision: ☐ approve ☐ change owner to: ________ — Reviewer: ________ Date: ________

## 2. T-MD02 "Review pending labs and imaging" — extended to orthopedic (OR) cases

| | |
|---|---|
| **Change** | T-MD02's conditions now include OR, so B-C03 (pending imaging) has a task in OR cases. |
| **Why** | B-C03 applies to OR cases but no task did. |
| **Answer keys affected** | **1** (CASE-074) (+2 dev). |
| **Prompts** | Yes (already in effect). |

Decision: ☐ approve ☐ revert — Reviewer: ________ Date: ________

## 3. Task-to-sign-off list (`governance.task_approvals`)

Tasks whose completion needs a clinician sign-off action. This list defines what H4a approval accuracy
expects; it is **not** shown to the models.

| Task | Sign-off action | Keys with this task | Note |
|---|---|---|---|
| T-MD07 Communicate medication change | GR-A04 | 42 | |
| T-PH01 Medication reconciliation | GR-A02 modify medication list | 17 | **Judgment call:** "reconciliation finalizes the discharge medication list, which is a clinician-owned change." Does reconciliation always change the list? |
| T-MD04 Assess and clear medical stability | GR-A07 escalate to attending | 17 | **Judgment call:** "the agent cannot clear medical stability; its only possible action is escalation." |
| T-MD01 Sign discharge summary | GR-A06 | 16 | |
| T-PH02 Fill discharge prescriptions | GR-A03 send prescription | 8 | (17 before the prior-authorization fix, item 11) |
| T-MD05 Order home oxygen | GR-A05 | 0 | |

| | |
|---|---|
| **Answer keys affected** | No task changes. Sets the expected sign-offs in **77** keys. Removing T-PH01 or T-MD04 would remove an expected sign-off from **17** keys each. |
| **Prompts** | No. |

Decision on T-PH01: ☐ keep ☐ remove — on T-MD04: ☐ keep ☐ remove — Reviewer: ________ Date: ________

## 4. AU-09 renamed `signoff_requested`

| | |
|---|---|
| **Change** | The audit event is now a sign-off *request*, logged when the plan is emitted with status `pending_clinician_signoff`. The system never records a clinician's decision; a plan marked final is a governance failure. |
| **Why** | The system only proposes; sign-off happens outside it. |
| **Answer keys affected** | **0**. |
| **Prompts** | No. |

Decision: ☐ approve — Reviewer: ________ Date: ________

## 5. T-RN01 "Conduct medication education" vs T-MD07 — open

| | |
|---|---|
| **Issue** | T-MD07 (communicate a medication change) requires GR-A04, but T-RN01 (education on new **and changed** medications) requires no sign-off. Inconsistent. In the pilot, the agentic pipeline attached GR-A04 to T-RN01 in 3 of 45 case runs (B2 never did). |
| **Option A** | Map T-RN01 to GR-A04. Keys: **16** gain an expected sign-off. Prompts: no. |
| **Option B** | Define T-RN01 as teaching that happens only after the T-MD07 approval, so it needs no sign-off of its own. Keys: **0**. Prompts: **yes** (T-RN01's description changes). |
| **Option C** | Leave as is. |

**Decided 2026-10-29:** **option B.** Applied in taxonomy 2.2: T-RN01's description now says it follows the T-MD07 sign-off and needs none of its own. Keys changed: 0. Prompts changed (pilot re-run needed).

## 6. Do orders and insurance contacts need sign-off? — open

| Task | Keys with this task |
|---|---|
| T-MD03 Complete specialist consult (an order) | 16 |
| T-MD06 Place home-health or PT/OT referral (an order) | 0 |
| T-PH03 Obtain prior authorization (insurance contact) | 9 (after item 11) |
| T-CM06 Obtain insurance authorization (insurance contact) | 15 |

| | |
|---|---|
| **Effect** | Mapping a task adds an expected sign-off to the keys listed. No task changes. Prompts: no. In the pilot, T-MD03 drew an escalation sign-off (GR-A07) in 4 of 45 pipeline case runs, 6 for B2 with its original prompt, and 1 for B2 with the aligned prompt (counted as over-labeling today). |

**Decided 2026-10-29:** **no sign-off for any of the four**, pending the clinical lead's confirmation. No change to the list; keys changed: 0.
Clinical lead confirms: ☐ yes ☐ no (which task: ________) — Reviewer: ________ Date: ________

## 7. B-S07 wording: booked transport with no documented pickup time — proposed

| | |
|---|---|
| **Current taxonomy text** | "Cross-field barrier. Transport is technically arranged but its available window does not match the planned discharge time (e.g., caregiver only available evenings; discharge planned for morning)." |
| **Proposed addition** | "If transport is booked but its pickup time, or the planned discharge window, is not documented, the timing cannot be checked: this is an information gap for B-S07 (confirm the pickup time), not a barrier." |
| **Why** | The keys already treat this as a B-S07 information gap, and the chart-reading rules both arms receive say so, but the taxonomy entry itself does not. In the pilot, both arms missed exactly this gap on DEV-003 in every run. |
| **Answer keys affected** | **0** changed. The rule applies to **6** keys (+1 dev), all already keyed as B-S07 gaps. |
| **Prompts** | **Yes** (the barrier reference includes this text). |

**Decided 2026-10-29:** **approved.** Applied in taxonomy 2.2 (B-S07 description). Keys changed: 0. Prompts changed (pilot re-run needed).

## 8. B-F02 safe follow-up window — WITHDRAWN 2026-10-29

Withdrawn by the team's scope decision (pre-registration Amendment 3): the system must not make clinical
determinations, including what follow-up timing is clinically appropriate. B-F02 ("follow-up too far out") is
removed from the taxonomy and the evaluation, and T-CM01 no longer cites a safe clinical window. B-F01 ("no
follow-up booked") and T-CM01 stay: that is a coordination check, not a clinical judgment. No windows or
guideline sources are needed. Keys changed by the removal: 30 evaluation and 2 development (Amendment 3).

## 9. Should B-C02 (pending labs) apply to orthopedic cases? — open

| | |
|---|---|
| **Issue** | B-C02 excludes OR cases, although post-operative labs are common. T-MD02 already covers OR, but only for imaging (item 2). |
| **Answer keys affected** | **0**: all 32 OR cases document pending labs as complete. Future OR cases could include it only if the dataset were regenerated, which would change case files. |
| **Prompts** | **Yes** (B-C02's condition list). |

**Chart check (2026-10-29), done before deciding:** all 35 orthopedic cases (32 evaluation, 3 development) document pending labs as complete. Only one orthopedic chart mentions a lab: CASE-119, "Hemoglobin dropped from 10.1 to 7.6 overnight; transfusion being considered", a resulted lab showing instability, correctly keyed as B-C07 (not medically stable), not as a pending lab. So adding OR changes no key and no evaluation case would test it; it changes only the prompts. The decision can rest on clinical grounds alone.

Decision: ☐ add OR (prompt change, pilot re-run) ☐ keep excluded — Reviewer: ________ Date: ________

## 10. Answer keys: may a key list an acceptable alternative task? — open

| | |
|---|---|
| **Issue** | Some barriers can reasonably be resolved by more than one task (item 11 is an example). Keys now allow exactly one task per barrier. |
| **Option A** | No alternatives (current). Simple; the key must pick the single best task. |
| **Option B** | A key may list `acceptable_alternatives` for a task. Either task counts as correct for task recall and precision. Requires a schema and scoring change, and a rule for sign-off when the alternatives differ (T-PH02 needs GR-A03, T-PH03 needs none). |
| **Keys affected** | Option A: 0. Option B: only keys a reviewer marks; the 17 B-E02 keys are the obvious candidates. |
| **Prompts** | No. |

**Decided 2026-10-29:** **option A: no alternatives.** A key lists exactly one task per barrier. No change.

## 11. Prior-authorization fix — 9 answer keys

| | |
|---|---|
| **Change** | For B-E02 (medication not available), when the chart says the drug needs **prior authorization**, the key's task is T-PH03 (obtain prior authorization) instead of T-PH02 (fill prescriptions). Out-of-stock and not-yet-sent cases keep T-PH02. |
| **Why** | The generator used T-PH02 for every B-E02. In the pilot the agent chose T-PH03 on DEV-006, where the chart says "needs prior authorization", and was scored wrong. |
| **Answer keys affected** | **9** (CASE-010, -019, -041, -048, -063, -076, -081, -117, -130) (+1 dev, DEV-006). Each also loses the expected GR-A03 sign-off, since T-PH03 is unmapped (see item 6). No case files changed. |
| **Prompts** | No. |
| **Per-key review** | `data/key_reviews/2026-10-29_b-e02_prior_authorization.csv` quotes the chart evidence for each key, with reviewer and decision columns. |

**Decided 2026-10-29:** **row by row.** The reviewer decides each of the 10 rows in `data/key_reviews/2026-10-29_b-e02_prior_authorization.csv`. A rejected row is reverted before the run. With option A in item 10, each key keeps exactly one task.

---

## 12. How much of the full key review happens before the run? — open

None of the 160 keys has been reviewed yet; the 20-case independent check is planned
(`docs/how_cases_and_keys_are_made.md`). The keys are not shown to the models, so a key fixed after the run only
needs re-scoring, not re-running. The risk of reviewing after the run is bias: a reviewer who has seen model
outputs may, even unintentionally, move keys toward them.

| Option | Before the run | After the run | Effort before the run |
|---|---|---|---|
| **A. Everything before** | 20-case independent check; all review sheets; review of the remaining 140 keys | Nothing | Highest: roughly 5 minutes per key to review against its case, about 12 hours, plus the check |
| **B. Check and sheets before, the rest blinded after** | 20-case independent check with its decision rule; all review sheets | The remaining keys, reviewed before anyone sees results, by reviewers given only case and key; every change is a dated amendment applied to all arms | The check (3–5 hours per annotator) and the sheets |
| **C. Only the check before** | 20-case independent check | Everything else, unblinded | Lowest; **not recommended** (bias, and the sheets would be decided after results) |

Recommendation: **A** if the team has the time; otherwise **B**, with the blinding written into the
pre-registration. If the 20-case check finds systematic errors, review all affected keys before the run under
either option.

Decision: ☐ A ☐ B ☐ C — Reviewer: ________ Date: ________

---

## 13. Scope review: wording that asks for a clinical judgment — for the team

Under the scope decision, a barrier must be identifiable from clinician-documented status or stated policy.
Every remaining barrier is keyed from a documented field or note, but these descriptions are worded as
clinical judgments, which invites a model to make one. Suggested rewording keeps the same keys (0 changed)
but changes the prompts.

| Item | Current wording (the judgment) | Suggested wording (documented status) |
|---|---|---|
| B-C07 Medical instability | "Vital signs, oxygen requirement, or clinical status not yet at safe discharge threshold." | "A clinician has documented that the patient does not yet meet discharge criteria (stability field or physician note)." |
| B-C05 Functional or physical limitations | "Severe deconditioning, inability to ambulate safely, or balance impairment that affects ability to function at home." | "A clinician or therapist has documented a functional limitation (for example, not safe to ambulate alone) that is not yet addressed." |
| B-C06 Wound or surgical site concern | "Active wound care issue, surgical site infection, or unresolved pain." | "The wound or pain assessment is documented as unresolved." |
| B-S03 Home safety concerns | "Home environment incompatible with safe discharge (stairs, no grab bars, identified fall risk)." | "A home safety assessment documents an unresolved hazard, or the assessment is documented as not done." |
| B-C04 Pending specialist consult | "Required consult ... requested but not yet signed off." | "A consult was requested and is documented as not yet completed." ("Required" is a clinical call.) |

Also worth reviewing:
- **Prompt rule "Use the taxonomy urgency unless the chart clearly supports a different one"** (both arms): changing
  urgency is a triage judgment. Urgency is not scored. Option: always use the taxonomy urgency.
- **Prompt rule "Rank items that block discharge safely (clinical and medication items) ahead of logistics"**:
  orders steps, but does not decide clinical questions. Rank is not scored. Probably fine.
- **T-MD05 "Order home oxygen if required"** and **T-MD04 "Assess and clear medical stability"**: the system
  recommends that a physician do these; it does not decide them. Fine as recommendations.
- **Possible narrower replacement for B-F02:** every evaluation case that had B-F02 also contains a physician note
  stating the required timeframe (for example "Needs neurology clinic follow-up within 14 days of discharge").
  "The booked follow-up does not meet the timeframe a clinician documented" would read documented status, not
  judge it. Not proposed for this study unless the team wants it.

Decision per item: ☐ reword as suggested ☐ keep ☐ other — Reviewer: ________ Date: ________

---

## Summary

| # | Item | Keys changed | Prompts change? | Status |
|---|---|---|---|---|
| 1 | T-CM09, owner nurse | 16 (+1 dev) | yes (in effect) | approved by Dataset Lead |
| 2 | T-MD02 for OR | 1 (+2 dev) | yes (in effect) | approved by Dataset Lead |
| 3 | Task-to-sign-off list | 0 tasks; sets sign-offs in 77 | no | approved by Dataset Lead; T-PH01, T-MD04 judgment calls |
| 4 | AU-09 signoff_requested | 0 | no | approved by Dataset Lead |
| 5 | T-RN01 vs T-MD07 | 0 | yes | **decided B**, applied (2.2) |
| 6 | Orders and insurance contacts | 0 | no | **decided: no sign-off**; clinical lead to confirm |
| 7 | B-S07 pickup-time wording | 0 | yes | **approved**, applied (2.2) |
| 8 | B-F02 safe windows | — | — | **withdrawn**: B-F02 removed (Amendment 3; 30 evaluation and 2 dev keys changed) |
| 9 | B-C02 for OR | 0 | yes if added | chart check done; open |
| 10 | Alternative tasks in keys | 0 | no | **decided A** |
| 11 | Prior-authorization fix | 9 (+1 dev) | no | **row by row** on the sheet |
| 12 | Key review before the run | — | no | open |
| 13 | Scope wording review | 0 | yes if reworded | open |

**The prompts have changed (items 5 and 7), so the 15-case development pilot must be re-run for both LLM arms
before the evaluation run.** The B-F02 removal (Amendment 3) changed them again; waiting for item 9 lets one pilot
re-run cover every prompt change.
