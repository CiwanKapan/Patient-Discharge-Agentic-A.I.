# CASE-132 — condition PN

**Planned discharge window:** 2026-05-27T13:00:00-05:00 to 2026-05-27T15:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete |  |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete |  |
| financial_status | complete |  |
| followup_appointment_status | unknown | detail: Not documented |
| home_health_referral_status | complete |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to a local independent pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-05-26T14:00:00-05:00 |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on completing the antibiotic course and pneumonia warning signs completed |
| pcp_notification_status | not_started | detail: PCP not yet notified of admission or medication changes |
| pending_consult | complete |  |
| pending_imaging | in_progress | detail: Repeat chest X-ray completed; awaiting radiology read |
| pending_labs | in_progress | detail: Legionella urine antigen resulted overnight but not yet reviewed by physician |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Medical transport to take patient home; window: {'start': '2026-05-27T14:00:00-05:00', 'end': '2026-05-27T15:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning. 5/26 18:00: Lisinopril changed from 20 mg daily to 10 mg daily on evening rounds. Patient and sister not yet told; this afternoon's teaching covered the old dose. Need to update the PCP before discharge.

**nursing_note**

Slept well overnight. Voiding without difficulty.

**physician_note**

68-year-old woman with hypertension, asthma, admitted 5/24 with left lower lobe pneumonia with small parapneumonic effusion. Leukocytosis resolved; tolerating diet. Pulse oximetry briefly read 94 percent during a deep sleep period overnight. Daytime readings have consistently been above 96 percent and no clinical concern was raised.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-C02 (single-field) — evidence: tracked_fields.pending_labs
- B-C03 (single-field) — evidence: tracked_fields.pending_imaging
- B-F05 (single-field) — evidence: tracked_fields.pcp_notification_status

**Information gaps**

- tracked_fields.followup_appointment_status → could indicate B-F01

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-MD02 resolves B-C02, B-C03
- T-CM08 resolves B-F05

**Must not flag (negative controls):** B-C07, B-F01
