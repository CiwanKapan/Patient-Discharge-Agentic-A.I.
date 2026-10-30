# CASE-125 — condition HF

**Planned discharge window:** 2026-03-16T09:00:00-05:00 to 2026-03-16T11:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Nephew will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | complete | detail: 2 g sodium and 2 L fluid restriction reviewed with teach-back |
| discharge_summary_status | complete |  |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Cardiology clinic visit booked; scheduled_for: 2026-03-20T08:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete |  |
| medication_education_status | in_progress | detail: Teaching on empagliflozin 10 mg daily started; teach-back not completed |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Nephrology signed off |
| pending_imaging | complete |  |
| pending_labs | in_progress | detail: Repeat BNP drawn this morning; result pending |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Nephew will pick patient up; window: {'start': '2026-03-16T17:00:00-05:00', 'end': '2026-03-16T18:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning. Physician to review the repeat BNP before discharge.

**nursing_note**

Slept well overnight. Voiding without difficulty. Patient asked what the new empagliflozin 10 mg daily is for; teaching still needed.

**physician_note**

66-year-old man with CAD s/p PCI, CKD stage 3, admitted 3/12 with HFpEF exacerbation precipitated by dietary sodium excess. Transitioned from IV to oral diuretic yesterday; weight stable. A venous thromboembolism risk assessment was completed on admission as per standard protocol. The patient received appropriate preventive measures during the stay. These are no longer needed after discharge.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, planned_discharge_window
- B-C02 (single-field) — evidence: tracked_fields.pending_labs
- B-E01 (single-field) — evidence: tracked_fields.medication_education_status

**Information gaps**

- none

**Tasks**

- T-CM04 resolves B-S07
- T-MD02 resolves B-C02
- T-RN01 resolves B-E01

**Must not flag (negative controls):** none
