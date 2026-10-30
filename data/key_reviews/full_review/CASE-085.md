# CASE-085 — condition PN

**Planned discharge window:** 2026-06-25T12:00:00-05:00 to 2026-06-25T14:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Daughter is primary caregiver; works days, available evenings; window: {'start': '2026-06-25T18:00:00-05:00', 'end': '2026-06-25T22:00:00-05:00'} |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | in_progress | detail: Discharge summary drafted; not signed |
| financial_status | complete |  |
| followup_appointment_status | in_progress | detail: Message sent to PCP for follow-up; no appointment confirmed |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to Walgreens; documented_at: 2026-06-24T10:00:00-05:00 |
| medication_education_status | complete |  |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on completing the antibiotic course and pneumonia warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | unknown | detail: No documentation found in chart |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Daughter to drive patient home after work; window: {'start': '2026-06-25T18:30:00-05:00', 'end': '2026-06-25T19:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with daughter. Still need to book the PCP appointment.

**nursing_note**

Slept well overnight. Voiding without difficulty. 6/25 09:20: Walgreens called: cefpodoxime is out of stock until next week. No alternate pharmacy arranged. The patient was treated for shingles approximately two years ago. The condition fully resolved and no residual effects were noted during this admission.

**physician_note**

71-year-old woman with dementia (mild), hypertension, admitted 6/19 with right lower lobe community-acquired pneumonia. Leukocytosis resolved; tolerating diet. Urine output was slightly lower than expected on the first night of admission. It has been normal and consistent since then.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, tracked_fields.caregiver_status, planned_discharge_window
- B-E02 (single-field) — evidence: tracked_fields.medication_availability_status, free_text_notes.nursing_note
- B-S06 (single-field) — evidence: tracked_fields.discharge_summary_status
- B-F01 (single-field) — evidence: tracked_fields.followup_appointment_status

**Information gaps**

- tracked_fields.medication_reconciliation_status → could indicate B-C01
- tracked_fields.pending_labs → could indicate B-C02

**Tasks**

- T-CM04 resolves B-S07
- T-PH02 resolves B-E02 — needs sign-off GR-A03 (send_prescription)
- T-MD01 resolves B-S06 — needs sign-off GR-A06 (sign_discharge_summary)
- T-CM01 resolves B-F01

**Must not flag (negative controls):** B-C01, B-C02, B-C07
