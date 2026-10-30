# CASE-026 — condition CO

**Planned discharge window:** 2026-06-01T14:00:00-05:00 to 2026-06-01T16:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Daughter will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Pulmonology clinic visit booked; scheduled_for: 2026-06-14T16:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to a local independent pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | in_progress | detail: Teaching on inhaler technique and the COPD action plan started; patient asked for daughter to be present for the rest |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Pulmonology signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Wheelchair van booked; window: {'start': '2026-06-02T14:30:00-05:00', 'end': '2026-06-02T15:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning.

**nursing_note**

Up in chair for meals. Pain controlled.

**physician_note**

83-year-old woman with anxiety, former smoker (40 pack-years), admitted 5/26 with COPD exacerbation triggered by viral bronchitis. Weaned from BiPAP on day 2; now on room air at rest. Sodium level was mildly below normal on the first blood draw. A repeat test the following morning showed it had corrected without any treatment.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, planned_discharge_window
- B-E03 (single-field) — evidence: tracked_fields.patient_education_status

**Information gaps**

- none

**Tasks**

- T-CM04 resolves B-S07
- T-RN02 resolves B-E03

**Must not flag (negative controls):** B-C02
