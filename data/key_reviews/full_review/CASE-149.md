# CASE-149 — condition CO

**Planned discharge window:** 2026-05-25T09:00:00-05:00 to 2026-05-25T11:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Son is primary caregiver |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete |  |
| financial_status | complete |  |
| followup_appointment_status | in_progress | detail: Message sent to pulmonology clinic for follow-up; no appointment confirmed |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to CVS |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-05-24T14:00:00-05:00 |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | complete | detail: Uses home oxygen 2 L/min at baseline; supply confirmed |
| patient_education_status | complete | detail: Teaching on inhaler technique and the COPD action plan completed |
| pcp_notification_status | complete |  |
| pending_consult | not_started | detail: Pulmonology consult ordered; patient not yet seen |
| pending_imaging | unknown | detail: Not documented |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Son to drive patient home; window: {'start': '2026-05-25T09:30:00-05:00', 'end': '2026-05-25T10:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and son to review the discharge plan. 5/24 19:00: Per pharmacy, prednisone taper: 30 mg x3 days, then 20 mg x3 days, then stop (was 40 mg daily). No documentation that the patient or family has been informed of the new dose. Earlier pickup was cancelled and rebooked for 09:30 to match the discharge time.

**nursing_note**

Ambulated in hallway with son present. Pulmonology has not seen the patient yet.

**physician_note**

56-year-old woman with osteoporosis, hypertension, admitted 5/21 with AECOPD with hypercapnic respiratory failure, now resolved. Completed 5 days of systemic steroids; wheeze resolved. The patient mentioned they have a COPD action plan at home that was written by their GP. They confirmed they are familiar with it and know when to seek help.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-F01 (single-field) — evidence: tracked_fields.followup_appointment_status
- B-C04 (single-field) — evidence: tracked_fields.pending_consult

**Information gaps**

- tracked_fields.pending_imaging → could indicate B-C03

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-CM01 resolves B-F01
- T-MD03 resolves B-C04

**Must not flag (negative controls):** B-C03, B-E03, B-S02, B-S07
