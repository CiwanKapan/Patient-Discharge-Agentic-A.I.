# CASE-130 — condition PN

**Planned discharge window:** 2026-05-04T12:00:00-05:00 to 2026-05-04T14:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Nephew will stay with patient for the first week |
| case_manager_status | not_started | detail: No case manager assigned to the unit this weekend |
| diet_education_status | not_applicable |  |
| discharge_summary_status | in_progress | detail: Discharge summary about 60% complete |
| financial_status | complete |  |
| followup_appointment_status | in_progress | detail: Message sent to pulmonology clinic for follow-up; no appointment confirmed |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Home pulse oximeter teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | not_started | detail: Amoxicillin-clavulanate 875/125 mg twice daily x5 days needs prior authorization; not available at a local independent pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-05-03T14:00:00-05:00 |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | in_progress | detail: Teaching on completing the antibiotic course and pneumonia warning signs started; patient asked for nephew to be present for the rest |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Infectious disease signed off |
| pending_imaging | complete |  |
| pending_labs | complete |  |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Nephew will pick patient up |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and nephew to review the discharge plan. 5/3 18:00: Lisinopril changed from 20 mg daily to 10 mg daily on evening rounds. Patient and nephew not yet told; this afternoon's teaching covered the old dose. Discharge paperwork still waiting on the summary.

**nursing_note**

Ambulated in hallway with nephew present. An infection control nurse completed a routine review of the patient's room and care on day 3. No concerns were identified and standard precautions are all in place. The patient is a smoker. Smoking cessation advice was offered and accepted. A referral to a cessation support service was made. This does not block discharge.

**physician_note**

60-year-old woman with dementia (mild), hypertension, admitted 4/30 with aspiration pneumonia, improving. Oxygen weaned to room air yesterday.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-F01 (single-field) — evidence: tracked_fields.followup_appointment_status
- B-E03 (single-field) — evidence: tracked_fields.patient_education_status
- B-E02 (single-field) — evidence: tracked_fields.medication_availability_status
- B-S05 (single-field) — evidence: tracked_fields.case_manager_status
- B-S06 (single-field) — evidence: tracked_fields.discharge_summary_status

**Information gaps**

- tracked_fields.transport_status → could indicate B-S07

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-CM01 resolves B-F01
- T-RN02 resolves B-E03
- T-PH03 resolves B-E02
- T-CM09 resolves B-S05
- T-MD01 resolves B-S06 — needs sign-off GR-A06 (sign_discharge_summary)

**Must not flag (negative controls):** B-S07
