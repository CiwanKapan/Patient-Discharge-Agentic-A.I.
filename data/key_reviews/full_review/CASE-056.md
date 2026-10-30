# CASE-056 — condition ST

**Planned discharge window:** 2026-04-20T13:00:00-05:00 to 2026-04-20T15:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Daughter is primary caregiver; works days, available evenings; window: {'start': '2026-04-20T18:00:00-05:00', 'end': '2026-04-20T22:00:00-05:00'} |
| case_manager_status | complete |  |
| diet_education_status | complete | detail: mechanical soft dysphagia diet with thin liquids reviewed with teach-back |
| discharge_summary_status | complete |  |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Neurology clinic visit booked; scheduled_for: 2026-04-27T13:00:00-05:00 |
| home_health_referral_status | complete |  |
| home_safety_status | complete | detail: Single-level home; grab bars installed |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Glucometer teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to CVS |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | complete | detail: Quad cane training completed with PT |
| outpatient_therapy_status | not_started | detail: Outpatient PT/OT referral not placed |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Cardiology (for loop recorder) signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Daughter to drive patient home after work; window: {'start': '2026-04-20T18:30:00-05:00', 'end': '2026-04-20T19:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and daughter to review the discharge plan.

**nursing_note**

Ambulated in hallway with daughter present. A routine palliative care screening question was included in the admission assessment as per standard protocol. The patient did not meet the criteria for a palliative care referral.

**physician_note**

63-year-old man with type 2 diabetes, hypertension, admitted 4/15 with left MCA ischemic stroke with mild right hemiparesis. Deficits stable for 48 hours; passed bedside swallow.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, tracked_fields.caregiver_status, planned_discharge_window
- B-F04 (single-field) — evidence: tracked_fields.outpatient_therapy_status

**Information gaps**

- none

**Tasks**

- T-CM04 resolves B-S07
- T-CM03 resolves B-F04

**Must not flag (negative controls):** none
