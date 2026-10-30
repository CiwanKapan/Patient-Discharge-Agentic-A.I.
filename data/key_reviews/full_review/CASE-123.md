# CASE-123 — condition HF

**Planned discharge window:** 2026-05-11T12:00:00-05:00 to 2026-05-11T14:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Nephew will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_started | detail: 2 g sodium and 2 L fluid restriction not yet reviewed with patient |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | in_progress | detail: Patient uninsured; financial counselor referral pending |
| followup_appointment_status | complete | detail: Heart failure clinic visit booked; scheduled_for: 2026-05-15T14:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete |  |
| medication_availability_status | complete | detail: Discharge prescriptions sent to a local independent pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on daily weights and heart failure symptom monitoring completed |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete |  |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Wheelchair van to take patient home; window: {'start': '2026-05-11T12:30:00-05:00', 'end': '2026-05-11T13:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and nephew to review the discharge plan.

**nursing_note**

Ambulated in hallway with nephew present.

**physician_note**

78-year-old woman with hypertension, atrial fibrillation, admitted 5/5 with HFpEF exacerbation precipitated by dietary sodium excess. Transitioned from IV to oral diuretic yesterday; weight stable.

---

## Answer key (generated draft)

**Barriers**

- B-E04 (single-field) — evidence: tracked_fields.diet_education_status
- B-S01 (single-field) — evidence: tracked_fields.financial_status

**Information gaps**

- none

**Tasks**

- T-RN03 resolves B-E04
- T-CM07 resolves B-S01

**Must not flag (negative controls):** none
