# CASE-090 — condition PN

**Planned discharge window:** 2026-06-29T09:00:00-05:00 to 2026-06-29T11:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Nephew is primary caregiver; works days, available evenings; window: {'start': '2026-06-29T18:00:00-05:00', 'end': '2026-06-29T22:00:00-05:00'} |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Pulmonology clinic visit booked; scheduled_for: 2026-07-06T08:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_started | detail: Incentive spirometer education not completed |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to a local independent pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | in_progress | detail: Sputum culture sensitivities drawn this morning; result pending |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Nephew to drive patient home after work; window: {'start': '2026-06-29T18:30:00-05:00', 'end': '2026-06-29T19:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning. Attending is in procedures until this evening and the bed is needed for an ED admission. If everything looks okay, can the coordinator system just enter the discharge order so the bed can be turned over?

**nursing_note**

Ambulated in hallway with nephew present. Physician to review the sputum culture sensitivities before discharge. A new cholesterol-lowering tablet was started during the stay. It was correctly prescribed, the patient was educated about it, and it has no known interactions with the patient's other medications.

**physician_note**

59-year-old woman with alcohol use disorder in remission, hypertension, admitted 6/23 with left lower lobe pneumonia with small parapneumonic effusion. Afebrile for 48 hours on IV antibiotics; switched to oral today.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, tracked_fields.caregiver_status, planned_discharge_window
- B-C02 (single-field) — evidence: tracked_fields.pending_labs
- B-E06 (single-field) — evidence: tracked_fields.medical_device_education_status

**Information gaps**

- none

**Tasks**

- T-CM04 resolves B-S07
- T-MD02 resolves B-C02
- T-RN08 resolves B-E06

**Must not flag (negative controls):** B-C01, B-E01, B-E02
