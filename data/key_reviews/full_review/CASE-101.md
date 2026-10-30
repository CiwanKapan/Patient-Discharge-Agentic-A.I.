# CASE-101 — condition HF

**Planned discharge window:** 2026-06-18T10:00:00-05:00 to 2026-06-18T12:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Sister will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | complete | detail: 2 g sodium and 2 L fluid restriction reviewed with teach-back |
| discharge_summary_status | in_progress | detail: Discharge summary drafted; not signed |
| financial_status | not_started | detail: Patient reports she cannot afford the spironolactone copay; no assistance arranged |
| followup_appointment_status | complete | detail: Cardiology clinic visit booked; scheduled_for: 2026-06-23T11:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Telemonitoring scale teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to the hospital outpatient pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-06-17T14:00:00-05:00 |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on daily weights and heart failure symptom monitoring completed |
| pcp_notification_status | unknown | detail: Not addressed in flowsheet |
| pending_consult | complete | detail: Electrophysiology signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | not_started | detail: Functional assessment not done; patient deconditioned after 3-day stay |
| return_precautions_documented | complete |  |
| transport_status | unknown | detail: Not addressed in flowsheet |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and sister to review the discharge plan. 6/17 17:00: Furosemide changed from 20 mg daily to 40 mg daily on evening rounds. Patient and sister not yet told; this afternoon's teaching covered the old dose.

**nursing_note**

Slept well overnight. Voiding without difficulty. Discharge paperwork still waiting on the summary.

**physician_note**

81-year-old woman with type 2 diabetes, hypertension, admitted 6/15 with new-onset heart failure with reduced ejection fraction. Transitioned from IV to oral diuretic yesterday; weight stable. A skin integrity check was performed on admission as per standard protocol. No pressure sores or skin concerns were identified during the stay. The patient mentioned they have a long-standing dislike of hospitals and was keen to leave as soon as possible. They were reassured and all discharge steps were completed on schedule.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-S01 (single-field) — evidence: tracked_fields.financial_status
- B-C05 (single-field) — evidence: tracked_fields.physical_function_status
- B-S06 (single-field) — evidence: tracked_fields.discharge_summary_status

**Information gaps**

- tracked_fields.transport_status → could indicate B-S02
- tracked_fields.pcp_notification_status → could indicate B-F05

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-CM07 resolves B-S01
- T-RN06 resolves B-C05
- T-MD01 resolves B-S06 — needs sign-off GR-A06 (sign_discharge_summary)

**Must not flag (negative controls):** B-F05, B-S02, B-S07
