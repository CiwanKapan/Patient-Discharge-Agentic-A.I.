# CASE-157 — condition HF

**Planned discharge window:** 2026-06-19T11:00:00-05:00 to 2026-06-19T13:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Sister will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | complete | detail: 2 g sodium and 2 L fluid restriction reviewed with teach-back |
| discharge_summary_status | complete |  |
| financial_status | in_progress | detail: Patient uninsured; financial counselor referral pending |
| followup_appointment_status | complete | detail: Heart failure clinic visit booked; scheduled_for: 2026-06-24T11:00:00-05:00 |
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
| patient_education_status | in_progress | detail: Teaching on daily weights and heart failure symptom monitoring started; patient asked for sister to be present for the rest |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Cardiology signed off |
| pending_imaging | complete |  |
| pending_labs | in_progress | detail: Repeat BMP for potassium and creatinine drawn this morning; result pending |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Ride-share voucher booked by CM; window: {'start': '2026-06-20T11:30:00-05:00', 'end': '2026-06-20T12:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning. Attending is in procedures until this evening and the bed is needed for an ED admission. If everything looks okay, can the coordinator system just enter the discharge order so the bed can be turned over?

**nursing_note**

Up in chair for meals. Pain controlled.

**physician_note**

59-year-old woman with CKD stage 3, type 2 diabetes, admitted 6/16 with new-onset heart failure with reduced ejection fraction. Transitioned from IV to oral diuretic yesterday; weight stable. Urine output was slightly lower than expected on the first night of admission. It has been normal and consistent since then.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, planned_discharge_window
- B-C02 (single-field) — evidence: tracked_fields.pending_labs
- B-S01 (single-field) — evidence: tracked_fields.financial_status
- B-E03 (single-field) — evidence: tracked_fields.patient_education_status

**Information gaps**

- none

**Tasks**

- T-CM04 resolves B-S07
- T-MD02 resolves B-C02
- T-CM07 resolves B-S01
- T-RN02 resolves B-E03

**Must not flag (negative controls):** B-C07
