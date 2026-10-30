# CASE-105 — condition ST

**Planned discharge window:** 2026-06-16T10:00:00-05:00 to 2026-06-16T12:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Nephew will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | complete | detail: mechanical soft dysphagia diet with thin liquids reviewed with teach-back |
| discharge_summary_status | complete |  |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Stroke clinic visit rebooked at patient request; scheduled_for: 2026-06-26T10:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | complete |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to CVS |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | complete | detail: Hemi-walker training completed with PT |
| outpatient_therapy_status | complete |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | not_started | detail: Carotid ultrasound ordered; not yet performed |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Nephew to drive patient home; documented_at: 2026-06-15T10:00:00-05:00; window: {'start': '2026-06-16T10:00:00-05:00', 'end': '2026-06-16T11:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning. 6/16 09:00: Nephew tested positive for COVID and cannot pick the patient up. Patient does not drive; no other ride identified. Radiology read on the carotid ultrasound still pending. Patient asked to move the stroke clinic appointment; rebooked within 14 days of discharge.

**nursing_note**

Slept well overnight. Voiding without difficulty.

**physician_note**

64-year-old woman with hyperlipidemia, hypertension, admitted 6/9 with left thalamic infarct with sensory deficits. Deficits stable for 48 hours; passed bedside swallow. The patient has a pet at home that requires daily feeding. This was discussed and the patient confirmed a neighbour has agreed to help with the pet until the patient is fully mobile.

---

## Answer key (generated draft)

**Barriers**

- B-S02 (single-field) — evidence: tracked_fields.transport_status, free_text_notes.case_manager_note
- B-C03 (single-field) — evidence: tracked_fields.pending_imaging

**Information gaps**

- tracked_fields.pcp_notification_status → could indicate B-F05

**Tasks**

- T-CM04 resolves B-S02
- T-MD02 resolves B-C03

**Must not flag (negative controls):** B-F01, B-F05
