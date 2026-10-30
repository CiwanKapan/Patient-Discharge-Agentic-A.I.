# CASE-019 — condition HF

**Planned discharge window:** 2026-03-25T10:00:00-05:00 to 2026-03-25T12:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | unknown | detail: No documentation found in chart |
| case_manager_status | in_progress | detail: Assigned case manager out sick; coverage not confirmed |
| diet_education_status | complete |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: PCP visit booked; scheduled_for: 2026-03-31T11:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Home scale and blood pressure cuff teaching done with return demonstration |
| medical_stability_status | complete |  |
| medication_availability_status | complete | detail: Discharge prescriptions sent to CVS; documented_at: 2026-03-24T07:00:00-05:00 |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | in_progress | detail: Teaching on daily weights and heart failure symptom monitoring started; patient asked for sister to be present for the rest |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Nephrology signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | not_started | detail: Functional assessment not done; patient deconditioned after 3-day stay |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Medical transport confirmed; window: {'start': '2026-03-25T16:00:00-05:00', 'end': '2026-03-25T17:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning.

**nursing_note**

Vitals stable this shift. Tolerating diet. 3/25 08:00: CVS reports empagliflozin needs prior authorization; claim rejected, patient cannot pick it up today. PT recommends assistance with all transfers for now. A low-grade temperature of 37.6 degrees was recorded on day 1. It resolved by day 2 without any treatment and has not returned.

**physician_note**

66-year-old man with atrial fibrillation, CKD stage 3, admitted 3/22 with HFpEF exacerbation precipitated by dietary sodium excess. Diuresed 6 kg with IV furosemide; now euvolemic on oral regimen. The patient's ejection fraction was rechecked on day 3 and found to be slightly improved from the admission value. This is a positive finding and does not change the discharge plan.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, planned_discharge_window
- B-E02 (single-field) — evidence: tracked_fields.medication_availability_status, free_text_notes.nursing_note
- B-C05 (single-field) — evidence: tracked_fields.physical_function_status
- B-E03 (single-field) — evidence: tracked_fields.patient_education_status
- B-S05 (single-field) — evidence: tracked_fields.case_manager_status

**Information gaps**

- tracked_fields.caregiver_status → could indicate B-F03

**Tasks**

- T-CM04 resolves B-S07
- T-PH03 resolves B-E02
- T-RN06 resolves B-C05
- T-RN02 resolves B-E03
- T-CM09 resolves B-S05

**Must not flag (negative controls):** B-C07, B-F03
