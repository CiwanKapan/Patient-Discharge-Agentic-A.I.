# Change log: differences from the original proposal and methodology

**Draft for mentor approval, together with `docs/preregistration.md`.** Prepared 2026-10-29, before any run on
the evaluation set.

**Baseline compared against.** The proposal and methodology documents are not in the repository (the
methodology's pre-registration section is to be added). This log compares against (a) the project as it stood
at commit `63a3cae`, including its README, which stated the plan, and (b) the methodology points known here:
the §7.6 success criteria and the requirement that answer keys be authored independently of the cases with
agreement measured. Items the mentor knows to differ from the methodology in other ways should be added.

**Amendment numbers.** Amendments 1 and 2 are already recorded in the pre-registration. Amendments 3–9 are
**proposed numbers**, grouping the remaining changes by theme; on approval they are recorded in the
pre-registration with these numbers and dates. All changes below were made on 2026-10-29.

| # | Original | Now | Reason | Amendment |
|---|---|---|---|---|
| **Dataset and answer keys** | | | | |
| 1 | 150 evaluation cases | 160 (10 added from a second seed, keeping 30/50/20 difficulty and balance across conditions; the original 150 unchanged) | Team request for more cases | **3** (proposed) |
| 2 | No development set; any pilot would use evaluation cases | 15 separate development cases (`data/dev/`); pilots and checks use only these | Keep the evaluation set unseen before the run | **3** (proposed) |
| 3 | Answer keys: one task per barrier from a fixed table; B-S05, and B-C03 in orthopedic cases, had no task | 17 keys gained a task (T-CM09 for B-S05 in 16; T-MD02 for B-C03 in 1) | Every barrier needs a task a correct system can propose | **4** (proposed) |
| 4 | B-E02 keyed to "fill prescriptions" whatever the chart said | Keyed to "obtain prior authorization" when the chart says so: 9 keys changed (review sheet pending) | The old keys penalized correct answers (found in the pilot) | **4** (proposed) |
| 5 | Keys to be reviewed by a team member other than the case author | Not yet done for any of the 160 keys. **Methodology deviation:** keys are generated with the cases from the same recipe, not authored independently, and agreement is not measured | Not yet addressed | **9** (proposed): a 20-case independent annotation with agreement measured before the run (`docs/how_cases_and_keys_are_made.md`) |
| **Taxonomy** | | | | |
| 6 | Taxonomy 2.0 (team's Word document) | 2.1: task-to-sign-off list, T-CM09 (owner: charge nurse), T-MD02 for orthopedic cases, AU-09 `signoff_requested`. Approved by the Dataset Lead 2026-10-29; further items pending (`docs/review_packet_2026-10-29.md`) | Fill coverage gaps; make sign-off requirements explicit and scorable | **4** (proposed) |
| **System architecture** | | | | |
| 7 | 8-stage pipeline | 9 stages: a sign-off request after the output composer. Every plan is emitted `pending_clinician_signoff`; a plan marked final is a governance failure | The team wants sign-off to occur after the output composer, outside the system | **5** (proposed) |
| 8 | Approval gate used only the model's own sign-off label | The gate also requires sign-off for tasks on the sign-off list when the model omits the label, and records the omission | A missing label scored as fully compliant (found in a test of incomplete responses) | **5** (proposed) |
| 9 | A barrier left without a task was silent | Listed in the plan as unaddressed, with a warning; duplicate task recommendations are rejected and re-asked | Make incomplete output visible | **5** (proposed) |
| **Baselines** | | | | |
| 10 | B2: no retries | B2 retries a response that does not parse, exactly as the pipeline does; only the pipeline retries content validation | Separate format robustness from scaffolding | **6** (proposed) |
| 11 | B2's prompt and output schema written separately from the pipeline's | B2 prompt v2: the pipeline's output instructions and schema word for word (`docs/arm_output_contract.md`) | B2 lacked about 15 instructions the pipeline has (19 recommendations dropped in the pilot); the arms should differ only in scaffolding | **6** (proposed) |
| 12 | — | B2 sent through the Batch API | Cost only; the requests are identical | **6** (proposed) |
| 13 | — | A third arm, B3 (B2 plus the pipeline's deterministic code), was considered and dropped before it ever ran | Team decision to keep two baselines | **6** (proposed) |
| **Run design and settings** | | | | |
| 14 | Model set in `.env` (`CLAUDE_MODEL`) | One shared settings file for every LLM arm: Claude Sonnet 5.5, medium effort, 16,000 max tokens, 2 attempts, no refusal fallback, prompt caching. Runs refuse to start if settings differ | Arms must use identical settings, and it must be provable | **7** (proposed) |
| 15 | One run per case (implied) | 3 runs per case for B2 and the pipeline; B1 once. A reduced design (1 run on all, 3 on a stratified 40) exists as a fallback but is not planned | LLM output varies between runs | **7** (proposed) |
| 16 | — | Prompts do not tell any arm which tasks need which sign-off action | Measure whether models infer sign-off needs themselves | **7** (proposed) |
| **Analysis** | | | | |
| 17 | H3 "plan completeness" undefined | Share of keyed tasks and information gaps that reached the plan as a recommendation | Make H3 measurable | **8** (proposed) |
| 18 | H4 "governance compliance" undefined; first implemented as a composite | **Primary: H4a approval accuracy** (recall on requires-approval actions over all keyed approval actions), with recall over recommended tasks, model labeling recall, forbidden-tool refusal (every temptation case), audit completeness, and the composite as secondary | The composite was decided by architecture: the baselines write no audit trail. The audit component favors the pipeline by design | **1** (recorded) |
| 19 | Strong success: "100% adherence to safety controls, large effect size" | Methodology §7.6: beats both baselines on at least 3 of H1–H4 with a non-negligible effect, and beats the strongest baseline on H4a by more than 0.2; mixed 1–2; null none | Restated in terms of approval accuracy | **1** (recorded) |
| 20 | — | Non-negligible effect: 95% bootstrap CI excludes zero and the difference is at least 0.05 (**pending mentor confirmation**); rank-biserial reported only | Make §7.6's "non-negligible" operational | **1** (recorded) |
| 21 | — | Outcome labels exhaustive (mixed = beats both on 1–4 without strong; null = on none), plus a reversal flag when a baseline beats the agentic system | §7.6 left two outcomes without a label; the dev pilot fell into one | **2** (recorded) |
| 22 | — | All tests two-sided; Wilcoxon signed-rank paired by case on the per-case mean over runs; Holm within a primary family (H1–H3, H4a vs B1 and B2) and a separate secondary family; precision and F1 for H1–H2 secondary | Fix the analysis before seeing results | **8** (proposed) |
| 23 | — | A failed or missing run is scored as an empty plan (infrastructure failures re-run first); over-labeling lowers approval precision only | Decide edge cases in advance | **8** (proposed) |
| 24 | — | Also reported: run-to-run variability, retries, items dropped, cost per case | Transparency | **8** (proposed) |

**Still open before the run** (see the pre-registration and the review packet): the 0.05 effect threshold;
the review packet items; the B-E02 key review sheet; the 20-case independent key check and its agreement
threshold (Amendment 9).
