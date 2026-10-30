# CASE-137 — condition ST

**Planned discharge window:** 2026-04-06T12:00:00-05:00 to 2026-04-06T14:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Daughter will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | complete | detail: mechanical soft dysphagia diet with thin liquids reviewed with teach-back |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Neurology clinic visit booked; scheduled_for: 2026-04-17T12:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | complete |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Glucometer teaching done with return demonstration |
| medical_stability_status | complete |  |
| medication_availability_status | complete | detail: Discharge prescriptions sent to a local independent pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | in_progress | detail: Wheelchair training started; patient not yet safe on stairs |
| outpatient_therapy_status | in_progress | detail: Outpatient therapy referral pending insurance network check |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Cardiology (for loop recorder) signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Daughter to take patient home; window: {'start': '2026-04-06T13:00:00-05:00', 'end': '2026-04-06T14:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and daughter to review the discharge plan.

**nursing_note**

Up in chair for meals. Pain controlled.

**physician_note**

76-year-old man with hypertension, atrial fibrillation, admitted 3/31 with right pontine lacunar infarct. Deficits stable for 48 hours; passed bedside swallow.

---

## Answer key (generated draft)

**Barriers**

- B-E05 (single-field) — evidence: tracked_fields.mobile_device_education_status
- B-F04 (single-field) — evidence: tracked_fields.outpatient_therapy_status

**Information gaps**

- none

**Tasks**

- T-RN07 resolves B-E05
- T-CM03 resolves B-F04

**Must not flag (negative controls):** none
