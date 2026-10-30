# CASE-072 — condition CO

**Planned discharge window:** 2026-03-05T15:00:00-05:00 to 2026-03-05T17:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete |  |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Pulmonology clinic visit booked; scheduled_for: 2026-03-18T16:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Home nebulizer teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete |  |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | complete | detail: Uses home oxygen 2 L/min at baseline; supply confirmed |
| patient_education_status | complete | detail: Teaching on inhaler technique and the COPD action plan completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Palliative care signed off |
| pending_imaging | complete |  |
| pending_labs | complete |  |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | in_progress | detail: Medicaid transport requested; not yet confirmed |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and son to review the discharge plan.

**nursing_note**

Vitals stable this shift. Tolerating diet.

**physician_note**

59-year-old man with GERD, anxiety, admitted 2/27 with acute exacerbation of COPD. Completed 5 days of systemic steroids; wheeze resolved.

---

## Answer key (generated draft)

**Barriers**

- B-S02 (single-field) — evidence: tracked_fields.transport_status

**Information gaps**

- none

**Tasks**

- T-CM04 resolves B-S02

**Must not flag (negative controls):** none
