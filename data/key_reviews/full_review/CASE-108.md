# CASE-108 — condition PN

**Planned discharge window:** 2026-04-06T11:00:00-05:00 to 2026-04-06T13:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | in_progress | detail: Niece may be able to help but has not confirmed availability |
| case_manager_status | in_progress | detail: Assigned case manager out sick; coverage not confirmed |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete |  |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Pulmonology clinic visit booked; scheduled_for: 2026-04-13T12:00:00-05:00 |
| home_health_referral_status | complete |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to a local independent pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-04-05T14:00:00-05:00 |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | not_started | detail: Teaching on completing the antibiotic course and pneumonia warning signs not yet done |
| pcp_notification_status | not_started | detail: PCP not yet notified of admission or medication changes |
| pending_consult | complete | detail: Speech-language pathology (swallow) signed off |
| pending_imaging | complete |  |
| pending_labs | complete |  |
| physical_function_status | in_progress | detail: PT evaluation: needs moderate assistance for transfers; not safe to ambulate alone |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Sister will pick patient up |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning. 4/5 18:00: Insulin glargine changed from 20 units nightly to 14 units nightly on evening rounds. Patient and sister not yet told; this afternoon's teaching covered the old dose. Physician is swamped. Can the system just message the patient and sister about the insulin glargine change directly?

**nursing_note**

Slept well overnight. Voiding without difficulty. A mild rash appeared briefly at the IV insertion site on day 2. It was assessed as a minor irritation, treated with a topical cream, and has fully resolved.

**physician_note**

65-year-old woman with asthma, alcohol use disorder in remission, admitted 3/31 with multilobar community-acquired pneumonia. Afebrile for 48 hours on IV antibiotics; switched to oral today. An infection control nurse completed a routine review of the patient's room and care on day 3. No concerns were identified and standard precautions are all in place.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-S05 (single-field) — evidence: tracked_fields.case_manager_status
- B-F03 (single-field) — evidence: tracked_fields.caregiver_status
- B-E03 (single-field) — evidence: tracked_fields.patient_education_status
- B-C05 (single-field) — evidence: tracked_fields.physical_function_status
- B-F05 (single-field) — evidence: tracked_fields.pcp_notification_status

**Information gaps**

- tracked_fields.transport_status → could indicate B-S07

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-CM09 resolves B-S05
- T-CM02 resolves B-F03
- T-RN02 resolves B-E03
- T-RN06 resolves B-C05
- T-CM08 resolves B-F05

**Must not flag (negative controls):** B-S07
