# Answer-key reviews

Each change to generated answer keys gets a review sheet here. Per the methodology, a team member other than
the case author must review every key; the reviewer fills in `reviewer`, `decision (accept/reject)`, and
`date` for each row and commits the sheet. A rejected row means the key change is reverted for that case
before any evaluation-set run.

| Sheet | Change | Cases | Status |
|---|---|---|---|
| `2026-10-29_b-e02_prior_authorization.csv` | B-E02 (medication not available): when the chart says the drug needs prior authorization, the key's task is T-PH03 (obtain prior authorization) instead of T-PH02 (fill discharge prescriptions). T-PH03 has no approval mapping, so GR-A03 is no longer expected for these cases. | 9 evaluation keys, 1 development key | Awaiting review; must be decided before the 160-case run |

How the change was made: `scripts/generate_cases.py` (`CaseBuilder.task_choices`) now picks the B-E02 task
from the barrier's own evidence text. It reads the finished case only, so no case file changed; regenerating
changed exactly the keys listed in the sheet and the expected-approval column of the two manifests.
