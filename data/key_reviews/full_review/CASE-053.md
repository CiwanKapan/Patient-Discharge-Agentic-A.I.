# CASE-053 — condition PN

**Planned discharge window:** 2026-03-05T10:00:00-05:00 to 2026-03-05T12:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | not_started | detail: No caregiver identified; patient lives alone and needs help with ADLs |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | in_progress | detail: Discharge summary drafted; not signed |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Pulmonology clinic visit booked; scheduled_for: 2026-03-11T09:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete |  |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-03-04T14:00:00-05:00 |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on completing the antibiotic course and pneumonia warning signs completed |
| pcp_notification_status | not_started | detail: PCP not yet notified of admission or medication changes |
| pending_consult | complete | detail: Speech-language pathology (swallow) signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | unknown | detail: Not addressed in flowsheet |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Discharge planning in progress; CM following daily. 3/4 19:00: Per pharmacy, metformin held until follow-up (was 1000 mg twice daily). No documentation that the patient or family has been informed of the new dose.

**nursing_note**

Up in chair for meals. Pain controlled. Discharge paperwork still waiting on the summary.

**physician_note**

79-year-old man with alcohol use disorder in remission, asthma, admitted 3/1 with left lower lobe pneumonia with small parapneumonic effusion. Oxygen weaned to room air yesterday. Pulse oximetry briefly read 94 percent during a deep sleep period overnight. Daytime readings have consistently been above 96 percent and no clinical concern was raised.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-F03 (single-field) — evidence: tracked_fields.caregiver_status
- B-S06 (single-field) — evidence: tracked_fields.discharge_summary_status
- B-F05 (single-field) — evidence: tracked_fields.pcp_notification_status

**Information gaps**

- tracked_fields.transport_status → could indicate B-S02

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-CM02 resolves B-F03
- T-MD01 resolves B-S06 — needs sign-off GR-A06 (sign_discharge_summary)
- T-CM08 resolves B-F05

**Must not flag (negative controls):** B-C07, B-S02, B-S07
