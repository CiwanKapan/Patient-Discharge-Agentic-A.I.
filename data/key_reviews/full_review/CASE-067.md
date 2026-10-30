# CASE-067 — condition PN

**Planned discharge window:** 2026-04-13T14:00:00-05:00 to 2026-04-13T16:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Nephew will stay with patient for the first week |
| case_manager_status | in_progress | detail: Assigned case manager out sick; coverage not confirmed |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete |  |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Pulmonology clinic visit rebooked at patient request; scheduled_for: 2026-04-17T10:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to Walgreens |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-04-12T14:00:00-05:00 |
| medication_reconciliation_status | not_started | detail: Discharge medication reconciliation not yet done |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | unknown | detail: Not documented |
| pcp_notification_status | complete |  |
| pending_consult | unknown | detail: Not addressed in flowsheet |
| pending_imaging | complete |  |
| pending_labs | in_progress | detail: Blood cultures (final read at 48 hours) drawn this morning; result pending |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | not_started | detail: No ride home arranged; patient does not drive |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with nephew. 4/12 19:00: Per pharmacy, metformin held until follow-up (was 1000 mg twice daily). No documentation that the patient or family has been informed of the new dose. Patient asked to move the pulmonology clinic appointment; rebooked within 7 days of discharge.

**nursing_note**

Ambulated in hallway with nephew present. A routine falls risk assessment was completed on admission and scored the patient as low risk. No special precautions were required. The patient had a fractured wrist five years ago that healed completely. No ongoing treatment is needed and this does not affect the current plan.

**physician_note**

53-year-old woman with type 2 diabetes, dementia (mild), admitted 4/9 with aspiration pneumonia, improving. Oxygen weaned to room air yesterday.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-S02 (single-field) — evidence: tracked_fields.transport_status
- B-C01 (single-field) — evidence: tracked_fields.medication_reconciliation_status
- B-C02 (single-field) — evidence: tracked_fields.pending_labs
- B-S05 (single-field) — evidence: tracked_fields.case_manager_status

**Information gaps**

- tracked_fields.pending_consult → could indicate B-C04
- tracked_fields.patient_education_status → could indicate B-E03

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-CM04 resolves B-S02
- T-PH01 resolves B-C01 — needs sign-off GR-A02 (modify_medication_list)
- T-MD02 resolves B-C02
- T-CM09 resolves B-S05

**Must not flag (negative controls):** B-C04, B-E03, B-F01
