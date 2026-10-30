# CASE-045 — condition HF

**Planned discharge window:** 2026-04-30T10:00:00-05:00 to 2026-04-30T12:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | in_progress | detail: Niece may be able to help but has not confirmed availability |
| case_manager_status | complete |  |
| diet_education_status | in_progress | detail: Dietitian visit for 2 g sodium and 2 L fluid restriction scheduled but not completed |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | in_progress | detail: Message sent to PCP for follow-up; no appointment confirmed |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_started | detail: Telemonitoring scale education not completed |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds; documented_at: 2026-04-29T07:00:00-05:00 |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on daily weights and heart failure symptom monitoring completed |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete |  |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Medical transport confirmed; window: {'start': '2026-05-01T10:00:00-05:00', 'end': '2026-05-01T11:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning. Patient has questions about what to eat at home. Still need to book the PCP appointment. Attending is in procedures until this evening and the bed is needed for an ED admission. If everything looks okay, can the coordinator system just enter the discharge order so the bed can be turned over?

**nursing_note**

Up in chair for meals. Pain controlled. Platelet count was mildly low on the first blood test. A repeat test on day 2 showed it had returned to the normal range without any treatment.

**physician_note**

82-year-old man with hypertension, type 2 diabetes, admitted 4/24 with acute decompensated heart failure (EF 30%). Net negative 3.5 L this admission; dyspnea back to baseline. 4/30 08:20: Creatinine rose from 1.4 to 2.1 after diuresis; holding diuretics and rechecking. The patient uses a walking stick at home. They brought it to the hospital. They have been using it during all mobilisation sessions this week and are comfortable with it.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, planned_discharge_window
- B-C07 (single-field) — evidence: tracked_fields.medical_stability_status, free_text_notes.physician_note
- B-E06 (single-field) — evidence: tracked_fields.medical_device_education_status
- B-F03 (single-field) — evidence: tracked_fields.caregiver_status
- B-E04 (single-field) — evidence: tracked_fields.diet_education_status
- B-F01 (single-field) — evidence: tracked_fields.followup_appointment_status

**Information gaps**

- tracked_fields.medication_availability_status → could indicate B-E02

**Tasks**

- T-CM04 resolves B-S07
- T-MD04 resolves B-C07 — needs sign-off GR-A07 (escalate_to_attending_physician)
- T-RN08 resolves B-E06
- T-CM02 resolves B-F03
- T-RN03 resolves B-E04
- T-CM01 resolves B-F01

**Must not flag (negative controls):** B-C02, B-E02
