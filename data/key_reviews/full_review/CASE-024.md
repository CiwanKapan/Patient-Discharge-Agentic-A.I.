# CASE-024 — condition CO

**Planned discharge window:** 2026-06-15T12:00:00-05:00 to 2026-06-15T14:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Nephew will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | not_started | detail: Patient reports she cannot afford the tiotropium copay; no assistance arranged |
| followup_appointment_status | in_progress | detail: Message sent to PCP for follow-up; no appointment confirmed |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds; documented_at: 2026-06-14T12:00:00-05:00 |
| medication_availability_status | complete | detail: Discharge prescriptions sent to Walgreens |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list, including the dose change; documented_at: 2026-06-14T15:00:00-05:00 |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | unknown | detail: No documentation found in chart |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Pulmonary rehabilitation signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | in_progress | detail: PT evaluation: needs moderate assistance for transfers; not safe to ambulate alone |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Medical transport to take patient home; window: {'start': '2026-06-15T12:30:00-05:00', 'end': '2026-06-15T13:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and nephew to review the discharge plan. Patient worried about the cost of the new medication. PT recommends assistance with all transfers for now.

**nursing_note**

Ambulated in hallway with nephew present. 6/14 15:00: Theophylline stopped (was 300 mg twice daily) this morning. Reviewed with patient and nephew at 15:00; teach-back correct.

**physician_note**

81-year-old woman with GERD, hypertension, admitted 6/8 with AECOPD with hypercapnic respiratory failure, now resolved. Completed 5 days of systemic steroids; wheeze resolved. 6/15 10:20: New wheeze and tachycardia (118) overnight; not at discharge threshold. A routine delirium screening was performed each morning as per standard protocol. The patient scored zero on every assessment and showed no signs of confusion.

---

## Answer key (generated draft)

**Barriers**

- B-C07 (single-field) — evidence: tracked_fields.medical_stability_status, free_text_notes.physician_note
- B-F01 (single-field) — evidence: tracked_fields.followup_appointment_status
- B-S01 (single-field) — evidence: tracked_fields.financial_status
- B-C05 (single-field) — evidence: tracked_fields.physical_function_status

**Information gaps**

- tracked_fields.patient_education_status → could indicate B-E03

**Tasks**

- T-MD04 resolves B-C07 — needs sign-off GR-A07 (escalate_to_attending_physician)
- T-CM01 resolves B-F01
- T-CM07 resolves B-S01
- T-RN06 resolves B-C05

**Must not flag (negative controls):** B-E01, B-E03, B-E07
