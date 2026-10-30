# CASE-027 — condition HF

**Planned discharge window:** 2026-06-22T13:00:00-05:00 to 2026-06-22T15:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Nephew will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_started | detail: 2 g sodium and 2 L fluid restriction not yet reviewed with patient |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Heart failure clinic visit booked; scheduled_for: 2026-06-29T12:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete |  |
| medical_stability_status | complete |  |
| medication_availability_status | complete | detail: Discharge prescriptions sent to the hospital outpatient pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on daily weights and heart failure symptom monitoring completed |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Wheelchair van booked; window: {'start': '2026-06-22T07:00:00-05:00', 'end': '2026-06-22T08:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning. Patient has questions about what to eat at home.

**nursing_note**

Slept well overnight. Voiding without difficulty. The patient's primary language is not English. A hospital interpreter was present for all key conversations during the stay, including all education sessions. All discharge information was provided in the patient's preferred language.

**physician_note**

71-year-old woman with CKD stage 3, CAD s/p PCI, admitted 6/18 with new-onset heart failure with reduced ejection fraction. Net negative 4.5 L this admission; dyspnea back to baseline.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, planned_discharge_window
- B-E04 (single-field) — evidence: tracked_fields.diet_education_status

**Information gaps**

- none

**Tasks**

- T-CM04 resolves B-S07
- T-RN03 resolves B-E04

**Must not flag (negative controls):** none
