# CASE-069 — condition CO

**Planned discharge window:** 2026-06-22T12:00:00-05:00 to 2026-06-22T14:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Nephew will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: PCP visit booked; scheduled_for: 2026-06-28T13:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Home nebulizer teaching done with return demonstration |
| medical_stability_status | complete |  |
| medication_availability_status | complete |  |
| medication_education_status | complete |  |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | in_progress | detail: Teaching on inhaler technique and the COPD action plan started; patient asked for nephew to be present for the rest |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | in_progress | detail: PT evaluation: needs moderate assistance for transfers; not safe to ambulate alone |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Nephew to take patient home; window: {'start': '2026-06-22T13:00:00-05:00', 'end': '2026-06-22T14:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with nephew.

**nursing_note**

Vitals stable this shift. Tolerating diet.

**physician_note**

78-year-old man with osteoporosis, anxiety, admitted 6/16 with acute exacerbation of COPD. Ambulated 100 m with PT yesterday without desaturation.

---

## Answer key (generated draft)

**Barriers**

- B-C05 (single-field) — evidence: tracked_fields.physical_function_status
- B-E03 (single-field) — evidence: tracked_fields.patient_education_status

**Information gaps**

- none

**Tasks**

- T-RN06 resolves B-C05
- T-RN02 resolves B-E03

**Must not flag (negative controls):** none
