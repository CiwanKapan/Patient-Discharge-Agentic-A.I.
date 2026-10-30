# CASE-049 — condition PN

**Planned discharge window:** 2026-03-02T14:00:00-05:00 to 2026-03-02T16:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Daughter will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Pulmonology clinic visit booked; scheduled_for: 2026-03-06T15:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to Walgreens |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on completing the antibiotic course and pneumonia warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | in_progress | detail: CT chest to exclude empyema completed; awaiting radiology read |
| pending_labs | complete |  |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Daughter to drive patient home; documented_at: 2026-03-01T13:00:00-05:00; window: {'start': '2026-03-02T14:00:00-05:00', 'end': '2026-03-02T15:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning. 3/2 11:45: Daughter called: car broke down, cannot come today. No alternative ride arranged yet.

**nursing_note**

Vitals stable this shift. Tolerating diet.

**physician_note**

72-year-old woman with hypertension, dementia (mild), admitted 2/27 with right lower lobe community-acquired pneumonia. Oxygen weaned to room air yesterday. The patient completed the full course of antibiotics during the admission. The infectious disease team confirmed no further antibiotic course is needed after discharge.

---

## Answer key (generated draft)

**Barriers**

- B-S02 (single-field) — evidence: tracked_fields.transport_status, free_text_notes.case_manager_note
- B-C03 (single-field) — evidence: tracked_fields.pending_imaging

**Information gaps**

- none

**Tasks**

- T-CM04 resolves B-S02
- T-MD02 resolves B-C03

**Must not flag (negative controls):** B-C01
