# CASE-114 — condition CO

**Planned discharge window:** 2026-06-22T11:00:00-05:00 to 2026-06-22T13:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete |  |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | in_progress | detail: Discharge summary about 60% complete |
| financial_status | complete |  |
| followup_appointment_status | in_progress | detail: Message sent to PCP for follow-up; no appointment confirmed |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete |  |
| medication_availability_status | complete | detail: Discharge prescriptions sent to Walgreens |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-06-21T14:00:00-05:00 |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | in_progress | detail: Teaching on inhaler technique and the COPD action plan started; patient asked for son to be present for the rest |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Son will pick patient up |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with son. 6/21 17:00: Per pharmacy, theophylline stopped (was 300 mg twice daily). No documentation that the patient or family has been informed of the new dose. Still need to book the PCP appointment.

**nursing_note**

Ambulated in hallway with son present. Discharge paperwork still waiting on the summary. The patient had a hernia repaired surgically four years ago. The repair was successful and the patient has had no recurrence. This is not relevant to the current discharge plan. The patient lives in a first-floor flat with no stairs. A home visit assessment was completed last year and confirmed the environment is safe and accessible.

**physician_note**

84-year-old woman with GERD, hypertension, admitted 6/19 with AECOPD with hypercapnic respiratory failure, now resolved. Weaned from BiPAP on day 2; now on room air at rest.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-F01 (single-field) — evidence: tracked_fields.followup_appointment_status
- B-S06 (single-field) — evidence: tracked_fields.discharge_summary_status
- B-E03 (single-field) — evidence: tracked_fields.patient_education_status

**Information gaps**

- tracked_fields.transport_status → could indicate B-S07

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-CM01 resolves B-F01
- T-MD01 resolves B-S06 — needs sign-off GR-A06 (sign_discharge_summary)
- T-RN02 resolves B-E03

**Must not flag (negative controls):** B-S07
