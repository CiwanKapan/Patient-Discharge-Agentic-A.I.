# How the 160 cases and their answer keys are produced

Written 2026-10-29 to plan a human check of answer-key agreement before the evaluation run.

## Short version

**One script, `scripts/generate_cases.py`, writes each case and its answer key together, from the same recipe,
in the same run.** The key is not read off the case afterwards; both are produced from one internal plan of what
the case should contain. That makes the keys consistent with the cases by construction, but **not independent
of them.** No person has yet authored or reviewed any of the 160 keys (the manifest's `validator` column is empty
for every case). The methodology's requirement, keys authored independently of the cases with agreement
measured, is **not met yet**; the human check below is how to address it.

## Who or what produces each part

| Part | Produced by | Written or reviewed by a person? |
|---|---|---|
| Taxonomy: barriers, tasks, sign-off actions, forbidden tools, audit events (`config/taxonomy.json`) | `scripts/build_config.py` converts the team's Word document; version 2.1 amendments are applied in the same script | **Yes.** The Word document is human-written; the 2.1 amendments were decided by the team and approved by the Dataset Lead on 2026-10-29 |
| Distractor phrases (`config/distractors.json`) | `scripts/build_config.py` from the team's distractor Word document | **Yes,** human-written |
| Case text templates: diagnoses, hospital courses, field details, note sentences for each barrier (inside `scripts/generate_cases.py`) | Written into the generator's code | **Written by a team member** (with AI assistance) as part of the generator; not separately reviewed |
| Which case gets which condition, difficulty, barriers, gaps, distractors, near-miss controls, temptation | `generate_cases.py`, from a fixed random seed and the dataset targets (30/50/20 difficulty, 32 per condition, every barrier used at least once) | No |
| The case itself: tracked fields, dates, free-text notes (`data/synthetic_cases/`) | `generate_cases.py`, filling the templates for the chosen recipe | No |
| The answer key: barriers with evidence, information gaps, tasks, must-not-flag controls (`data/answer_keys/`) | `generate_cases.py`, **from the same recipe**: each barrier it wrote into the case is keyed; tasks come from a fixed barrier-to-task table (`TASKS_FOR`, plus the reason-dependent B-E02 rule); expected sign-offs follow the taxonomy's task-to-sign-off list | **No.** Keys are drafts. Changes since generation go through review sheets in `data/key_reviews/` (one pending) |
| Consistency checks | The generator's own `validate()`, and `tests/test_synthetic_cases.py` (written separately so the generator does not grade itself) | Code checks only: they confirm the keys follow the rules (for example an undocumented field is a gap, never a barrier); they do not judge clinical correctness |
| Development set (`data/dev/`, 15 cases) | The same generator, its own seed | No; used only for pilots |

## Step by step

1. **Plan the dataset.** From a fixed seed, the generator assigns each case a condition and difficulty (150 main
   cases, plus 10 added from a second seed).
2. **Choose the recipe.** For each case it chooses barriers (more and harder ones for higher difficulty, including
   cross-field and note-only barriers), information gaps (fields left undocumented on purpose), near-miss
   controls, distractor phrases, and sometimes a note tempting toward a forbidden tool.
3. **Write the case.** It fills every tracked field: complete by default, not done for each chosen barrier,
   undocumented for each chosen gap. It then writes the free-text notes from the templates, including the
   evidence for note-only and cross-field barriers, the distractors, and the temptation.
4. **Write the key from the same recipe.** Every chosen barrier becomes a keyed barrier with the fields the
   generator wrote as evidence. Every chosen gap becomes a keyed information gap. Tasks come from the
   barrier-to-task table. Negative controls go to must-not-flag.
5. **Validate and write.** Each case and key is checked against the data models and the dataset rules; if any
   fails, nothing is written. Re-running the command reproduces the same files.

## What this means for the human check

Because the key is derived from the recipe, the generator and the key share every assumption: if a template
sentence reads differently from what the recipe intended, the key cannot notice. The prior-authorization
problem was exactly this kind of error: the chart said "needs prior authorization", the key said "fill
prescriptions", and nobody reading the case independently had checked it. An independent check should
therefore start from the **case text only**.

### Proposed protocol for the 20-case check (for the team to adjust)

- **Sample:** 20 evaluation cases, stratified: 4 per condition, 6 easy / 10 medium / 4 hard, and including at
  least a few of each: cross-field barriers (B-S07, B-E07), note-only barriers, information gaps, near-miss
  controls, and temptation cases. Drawn from a fixed seed and recorded before anyone looks at keys.
- **Annotators:** two people who did not write the generator, working separately, ideally including the
  clinical lead.
- **What they see:** the case as the models see it (difficulty and distractor labels removed), taxonomy 2.1, and
  the same chart-reading rules the models get. Not the keys, the manifest, or any model output.
- **What they write:** for each case, the barriers (with the field or note supporting each), the information
  gaps, and the task for each barrier. Sign-off expectations follow from the tasks and need not be annotated.
- **What is measured:** agreement between each annotator and the generated key, and between the two
  annotators: per case and barrier ID (present or not), Cohen's kappa and positive agreement; the same for
  information gaps and tasks.
- **Decision rule (to agree before the check):** for example, accept the keys if annotator-key agreement is at or
  above an agreed kappa; adjudicate every disagreement; where a disagreement reveals a systematic generator
  error, fix the generator, regenerate the keys (cases unchanged), and send the changes through a review sheet.
- **Effort:** roughly 10–15 minutes per case per annotator, so about 3–5 hours each.

I can prepare the stratified 20-case list, a blinded annotation packet, an annotation template, and an
agreement script, none of which call a model.
