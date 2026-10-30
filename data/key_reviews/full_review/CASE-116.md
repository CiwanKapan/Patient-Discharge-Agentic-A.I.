# CASE-116 — condition HF

**Planned discharge window:** 2026-05-04T11:00:00-05:00 to 2026-05-04T13:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Son will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | complete | detail: 2 g sodium and 2 L fluid restriction reviewed with teach-back |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | not_started | detail: Patient reports he cannot afford the sacubitril/valsartan copay; no assistance arranged |
| followup_appointment_status | complete | detail: Cardiology clinic visit booked; scheduled_for: 2026-05-08T10:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to Walgreens |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on daily weights and heart failure symptom monitoring completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Cardiology signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | not_started | detail: No ride home arranged; patient does not drive |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning.

**nursing_note**

Up in chair for meals. Pain controlled.

**physician_note**

77-year-old man with hypertension, type 2 diabetes, admitted 4/27 with new-onset heart failure with reduced ejection fraction. Net negative 5.3 L this admission; dyspnea back to baseline.

---

## Answer key (generated draft)

**Barriers**

- B-S01 (single-field) — evidence: tracked_fields.financial_status
- B-S02 (single-field) — evidence: tracked_fields.transport_status

**Information gaps**

- none

**Tasks**

- T-CM07 resolves B-S01
- T-CM04 resolves B-S02

**Must not flag (negative controls):** none
