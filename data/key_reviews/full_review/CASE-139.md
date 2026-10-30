# CASE-139 — condition OR

**Planned discharge window:** 2026-05-29T08:00:00-05:00 to 2026-05-29T10:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Nephew is primary caregiver |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete |  |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Orthopedic surgery clinic visit rebooked at patient request; scheduled_for: 2026-06-07T10:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | complete | detail: Single-level home; grab bars installed |
| insurance_authorization_status | in_progress | detail: Insurance authorization for short-term rehab placement pending |
| medical_device_education_status | complete | detail: Continuous passive motion machine teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to Walgreens |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-05-28T14:00:00-05:00 |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | complete | detail: Knee scooter training completed with PT |
| outpatient_therapy_status | complete |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Physical medicine and rehabilitation signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Nephew to drive patient home; window: {'start': '2026-05-29T08:30:00-05:00', 'end': '2026-05-29T09:30:00-05:00'} |
| wound_status | complete | detail: Incision clean, dry and intact |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning. 5/28 18:00: Metoprolol tartrate changed from 25 mg twice daily to 12.5 mg twice daily on evening rounds. Patient and nephew not yet told; this afternoon's teaching covered the old dose. Original evening van slot cancelled; family will drive at the planned discharge time instead. Patient asked to move the orthopedic surgery clinic appointment; rebooked within 14 days of discharge.

**nursing_note**

Vitals stable this shift. Tolerating diet. A skin integrity check was performed on admission as per standard protocol. No pressure sores or skin concerns were identified during the stay.

**physician_note**

84-year-old woman with hypertension, osteoarthritis, admitted 5/24 for right hip hemiarthroplasty after femoral neck fracture. Post-op day 4; working with PT twice daily.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-S04 (single-field) — evidence: tracked_fields.insurance_authorization_status

**Information gaps**

- none

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-CM06 resolves B-S04

**Must not flag (negative controls):** B-C06, B-F01, B-S02, B-S07
