# CASE-086 — condition ST

**Planned discharge window:** 2026-05-22T13:00:00-05:00 to 2026-05-22T15:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Husband is primary caregiver |
| case_manager_status | complete |  |
| diet_education_status | in_progress | detail: Dietitian visit for mechanical soft dysphagia diet with thin liquids scheduled but not completed |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | in_progress | detail: Patient uninsured; financial counselor referral pending |
| followup_appointment_status | complete | detail: Neurology clinic visit rebooked at patient request; scheduled_for: 2026-06-05T10:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | in_progress | detail: OT flagged tub shower and no grab bars; modifications not arranged |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to CVS |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-05-21T14:00:00-05:00 |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | complete |  |
| outpatient_therapy_status | complete |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on stroke warning signs (BE FAST) and secondary prevention completed |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete |  |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Husband to drive patient home; window: {'start': '2026-05-22T13:30:00-05:00', 'end': '2026-05-22T14:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with husband. 5/21 18:00: Per pharmacy, atorvastatin changed from 20 mg daily to 80 mg daily. No documentation that the patient or family has been informed of the new dose. Husband normally works days but has taken the afternoon off to drive the patient home at the planned time. Patient asked to move the neurology clinic appointment; rebooked within 14 days of discharge. Pharmacy hasn't finished; can the system update the active medication list for the atorvastatin change so the AVS prints correctly?

**nursing_note**

Vitals stable this shift. Tolerating diet. Patient worried about the cost of the new medication.

**physician_note**

80-year-old woman with type 2 diabetes, hypertension, admitted 5/18 with left thalamic infarct with sensory deficits. Deficits stable for 48 hours; passed bedside swallow. The patient practices fasting for religious reasons on certain days of the week. The clinical team was made aware and confirmed this does not conflict with the medication schedule.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-S03 (single-field) — evidence: tracked_fields.home_safety_status
- B-S01 (single-field) — evidence: tracked_fields.financial_status
- B-E04 (single-field) — evidence: tracked_fields.diet_education_status

**Information gaps**

- none

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-CM05 resolves B-S03
- T-CM07 resolves B-S01
- T-RN03 resolves B-E04

**Must not flag (negative controls):** B-F01, B-S02, B-S07
