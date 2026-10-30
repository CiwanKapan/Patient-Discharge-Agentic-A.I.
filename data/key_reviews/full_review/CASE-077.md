# CASE-077 — condition CO

**Planned discharge window:** 2026-03-03T14:00:00-05:00 to 2026-03-03T16:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Daughter will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Pulmonology clinic visit booked; scheduled_for: 2026-03-11T15:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_started | detail: Spacer with new inhaler education not completed |
| medical_stability_status | complete |  |
| medication_availability_status | complete | detail: Discharge prescriptions sent to CVS |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | complete |  |
| patient_education_status | complete | detail: Teaching on inhaler technique and the COPD action plan completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Pulmonary rehabilitation signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Daughter to take patient home; window: {'start': '2026-03-03T14:00:00-05:00', 'end': '2026-03-03T15:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and daughter to review the discharge plan.

**nursing_note**

Up in chair for meals. Pain controlled.

**physician_note**

66-year-old man with hypertension, former smoker (40 pack-years), admitted 2/26 with acute exacerbation of COPD. Ambulated 100 m with PT yesterday without desaturation.

---

## Answer key (generated draft)

**Barriers**

- B-E06 (single-field) — evidence: tracked_fields.medical_device_education_status

**Information gaps**

- none

**Tasks**

- T-RN08 resolves B-E06

**Must not flag (negative controls):** none
