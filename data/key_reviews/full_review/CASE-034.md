# CASE-034 — condition ST

**Planned discharge window:** 2026-05-14T09:00:00-05:00 to 2026-05-14T11:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Husband will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | complete | detail: mechanical soft dysphagia diet with thin liquids reviewed with teach-back |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | in_progress | detail: Patient uninsured; financial counselor referral pending |
| followup_appointment_status | complete | detail: Neurology clinic visit rebooked at patient request; scheduled_for: 2026-05-24T10:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | complete | detail: Single-level home; grab bars installed |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete |  |
| medication_availability_status | complete | detail: Discharge prescriptions sent to a local independent pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_started | detail: Quad cane education not done |
| outpatient_therapy_status | not_started | detail: Outpatient PT/OT referral not placed |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on stroke warning signs (BE FAST) and secondary prevention completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Neurology signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Ride-share voucher booked by CM; window: {'start': '2026-05-15T09:00:00-05:00', 'end': '2026-05-15T10:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and husband to review the discharge plan. Patient asked to move the neurology clinic appointment; rebooked within 14 days of discharge.

**nursing_note**

Up in chair for meals. Pain controlled. Patient's potassium was mildly low on day 2 of admission but was corrected with an oral supplement. It was rechecked on day 3 and returned to the normal range.

**physician_note**

53-year-old woman with type 2 diabetes, hyperlipidemia, admitted 5/11 with small right cerebellar infarct. NIHSS improved from 6 to 2.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, planned_discharge_window
- B-F04 (single-field) — evidence: tracked_fields.outpatient_therapy_status
- B-E05 (single-field) — evidence: tracked_fields.mobile_device_education_status
- B-S01 (single-field) — evidence: tracked_fields.financial_status

**Information gaps**

- none

**Tasks**

- T-CM04 resolves B-S07
- T-CM03 resolves B-F04
- T-RN07 resolves B-E05
- T-CM07 resolves B-S01

**Must not flag (negative controls):** B-C02, B-F01
