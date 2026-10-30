# CASE-155 — condition OR

**Planned discharge window:** 2026-05-29T14:00:00-05:00 to 2026-05-29T16:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Nephew is primary caregiver |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | in_progress | detail: Discharge summary drafted; not signed |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Orthopedic surgery clinic visit rebooked at patient request; scheduled_for: 2026-06-08T10:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_started | detail: Lives in second-floor walk-up; stairs and bathroom not assessed |
| insurance_authorization_status | complete |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to a local independent pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-05-28T14:00:00-05:00 |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | complete | detail: Rolling walker training completed with PT |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Wound care signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Nephew to drive patient home; window: {'start': '2026-05-29T14:30:00-05:00', 'end': '2026-05-29T15:30:00-05:00'} |
| wound_status | complete | detail: Incision clean, dry and intact |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with nephew. 5/28 18:00: Metoprolol tartrate changed from 25 mg twice daily to 12.5 mg twice daily on evening rounds. Patient and nephew not yet told; this afternoon's teaching covered the old dose. Discharge paperwork still waiting on the summary. Earlier pickup was cancelled and rebooked for 14:30 to match the discharge time. Patient asked to move the orthopedic surgery clinic appointment; rebooked within 14 days of discharge.

**nursing_note**

Slept well overnight. Voiding without difficulty. Bedroom is upstairs at home; setup not reviewed yet.

**physician_note**

61-year-old woman with hypothyroidism, obesity, admitted 5/24 for left total hip arthroplasty. Post-op day 4; working with PT twice daily. A low-grade temperature of 37.6 degrees was recorded on day 1. It resolved by day 2 without any treatment and has not returned.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-S03 (single-field) — evidence: tracked_fields.home_safety_status
- B-S06 (single-field) — evidence: tracked_fields.discharge_summary_status

**Information gaps**

- none

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-CM05 resolves B-S03
- T-MD01 resolves B-S06 — needs sign-off GR-A06 (sign_discharge_summary)

**Must not flag (negative controls):** B-C07, B-F01, B-S02, B-S07
