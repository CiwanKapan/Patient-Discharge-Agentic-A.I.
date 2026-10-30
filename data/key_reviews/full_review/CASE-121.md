# CASE-121 — condition PN

**Planned discharge window:** 2026-06-26T15:00:00-05:00 to 2026-06-26T17:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | not_started | detail: No caregiver identified; patient lives alone and needs help with ADLs |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | unknown | detail: Not addressed in flowsheet |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: PCP visit rebooked at patient request; scheduled_for: 2026-07-01T10:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Incentive spirometer teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to the hospital outpatient pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-06-25T14:00:00-05:00 |
| medication_reconciliation_status | not_started | detail: Discharge medication reconciliation not yet done |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on completing the antibiotic course and pneumonia warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Pulmonology signed off |
| pending_imaging | not_started | detail: Repeat chest X-ray ordered; not yet performed |
| pending_labs | unknown | detail: No documentation found in chart |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Wheelchair van to take patient home; window: {'start': '2026-06-26T15:30:00-05:00', 'end': '2026-06-26T16:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Discharge planning in progress; CM following daily. 6/25 18:00: Per pharmacy, insulin glargine changed from 20 units nightly to 14 units nightly. No documentation that the patient or family has been informed of the new dose. Radiology read on the repeat chest X-ray still pending. Patient asked to move the PCP appointment; rebooked within 7 days of discharge.

**nursing_note**

Vitals stable this shift. Tolerating diet. The patient experienced a fall at home approximately six months ago. There have been no falls during this admission. Home safety was assessed and no concerns were identified. The patient practices fasting for religious reasons on certain days of the week. The clinical team was made aware and confirmed this does not conflict with the medication schedule.

**physician_note**

73-year-old woman with asthma, dementia (mild), admitted 6/20 with aspiration pneumonia, improving. Leukocytosis resolved; tolerating diet.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-C03 (single-field) — evidence: tracked_fields.pending_imaging
- B-C01 (single-field) — evidence: tracked_fields.medication_reconciliation_status
- B-F03 (single-field) — evidence: tracked_fields.caregiver_status

**Information gaps**

- tracked_fields.pending_labs → could indicate B-C02
- tracked_fields.discharge_summary_status → could indicate B-S06

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-MD02 resolves B-C03
- T-PH01 resolves B-C01 — needs sign-off GR-A02 (modify_medication_list)
- T-CM02 resolves B-F03

**Must not flag (negative controls):** B-C02, B-F01, B-S06
