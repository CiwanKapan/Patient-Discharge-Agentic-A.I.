# CASE-022 — condition PN

**Planned discharge window:** 2026-03-04T15:00:00-05:00 to 2026-03-04T17:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Son will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | in_progress | detail: Discharge summary about 60% complete |
| financial_status | in_progress | detail: Patient uninsured; financial counselor referral pending |
| followup_appointment_status | complete | detail: PCP visit booked; scheduled_for: 2026-03-10T15:00:00-05:00 |
| home_health_referral_status | complete |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete |  |
| medication_education_status | in_progress | detail: Teaching on amoxicillin-clavulanate 875/125 mg twice daily x5 days started; teach-back not completed |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on completing the antibiotic course and pneumonia warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Speech-language pathology (swallow) signed off |
| pending_imaging | complete |  |
| pending_labs | complete |  |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Son to drive patient home; documented_at: 2026-03-03T12:00:00-05:00; window: {'start': '2026-03-04T15:00:00-05:00', 'end': '2026-03-04T16:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with son. 3/4 12:45: Son tested positive for COVID and cannot pick the patient up. Patient does not drive; no other ride identified. Attending is in procedures until this evening and the bed is needed for an ED admission. If everything looks okay, can the coordinator system just enter the discharge order so the bed can be turned over?

**nursing_note**

Up in chair for meals. Pain controlled.

**physician_note**

69-year-old woman with asthma, dementia (mild), admitted 2/26 with right lower lobe community-acquired pneumonia. Leukocytosis resolved; tolerating diet. A chest X-ray taken on admission showed mild changes. A repeat X-ray on day 3 shows significant improvement and the radiologist has cleared the patient for discharge.

---

## Answer key (generated draft)

**Barriers**

- B-S02 (single-field) — evidence: tracked_fields.transport_status, free_text_notes.case_manager_note
- B-S01 (single-field) — evidence: tracked_fields.financial_status
- B-S06 (single-field) — evidence: tracked_fields.discharge_summary_status
- B-E01 (single-field) — evidence: tracked_fields.medication_education_status

**Information gaps**

- none

**Tasks**

- T-CM04 resolves B-S02
- T-CM07 resolves B-S01
- T-MD01 resolves B-S06 — needs sign-off GR-A06 (sign_discharge_summary)
- T-RN01 resolves B-E01

**Must not flag (negative controls):** B-C03
