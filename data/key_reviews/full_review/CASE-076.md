# CASE-076 — condition CO

**Planned discharge window:** 2026-06-24T09:00:00-05:00 to 2026-06-24T11:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | in_progress | detail: Niece may be able to help but has not confirmed availability |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete |  |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Pulmonology clinic visit booked; scheduled_for: 2026-07-06T11:00:00-05:00 |
| home_health_referral_status | complete |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Spacer with new inhaler teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | not_started | detail: Azithromycin 250 mg three times weekly needs prior authorization; not available at a local independent pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-06-23T14:00:00-05:00 |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | complete |  |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Pulmonology signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Daughter to take patient home; window: {'start': '2026-06-24T09:30:00-05:00', 'end': '2026-06-24T10:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning. 6/23 17:00: Per pharmacy, theophylline stopped (was 300 mg twice daily). No documentation that the patient or family has been informed of the new dose. Patient's pharmacy cannot fill the new prescription yet.

**nursing_note**

Up in chair for meals. Pain controlled.

**physician_note**

75-year-old man with former smoker (40 pack-years), osteoporosis, admitted 6/17 with acute exacerbation of COPD. Ambulated 100 m with PT yesterday without desaturation. The patient reported a mild reaction to a type of antibiotic many years ago. This is documented in the records. The antibiotic used in this admission is from a different family and no reaction occurred.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-E02 (single-field) — evidence: tracked_fields.medication_availability_status
- B-F03 (single-field) — evidence: tracked_fields.caregiver_status

**Information gaps**

- none

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-PH03 resolves B-E02
- T-CM02 resolves B-F03

**Must not flag (negative controls):** none
