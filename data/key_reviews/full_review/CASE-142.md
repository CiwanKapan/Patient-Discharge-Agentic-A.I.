# CASE-142 — condition ST

**Planned discharge window:** 2026-06-12T15:00:00-05:00 to 2026-06-12T17:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Nephew will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | complete |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Neurology clinic visit rebooked at patient request; scheduled_for: 2026-06-17T10:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | complete | detail: Single-level home; grab bars installed |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_started | detail: Home blood pressure monitor education not completed |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to the hospital outpatient pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | complete | detail: Wheelchair training completed with PT |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on stroke warning signs (BE FAST) and secondary prevention completed |
| pcp_notification_status | complete |  |
| pending_consult | not_started | detail: Speech-language pathology consult ordered; patient not yet seen |
| pending_imaging | complete |  |
| pending_labs | complete |  |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Nephew will pick patient up before work; window: {'start': '2026-06-12T07:00:00-05:00', 'end': '2026-06-12T08:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and nephew to review the discharge plan. Patient asked to move the neurology clinic appointment; rebooked within 14 days of discharge.

**nursing_note**

Slept well overnight. Voiding without difficulty.

**physician_note**

86-year-old man with hyperlipidemia, prior TIA, admitted 6/7 with right pontine lacunar infarct. Deficits stable for 48 hours; passed bedside swallow. The patient has a well-healed surgical scar on the abdomen from an operation several years ago. No wound care is needed and this has no impact on the discharge plan.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, planned_discharge_window
- B-C04 (single-field) — evidence: tracked_fields.pending_consult
- B-E06 (single-field) — evidence: tracked_fields.medical_device_education_status

**Information gaps**

- none

**Tasks**

- T-CM04 resolves B-S07
- T-MD03 resolves B-C04
- T-RN08 resolves B-E06

**Must not flag (negative controls):** B-F01
