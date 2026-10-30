# CASE-124 — condition ST

**Planned discharge window:** 2026-03-24T14:00:00-05:00 to 2026-03-24T16:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Son will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | complete |  |
| discharge_summary_status | in_progress | detail: Discharge summary about 60% complete |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Stroke clinic visit booked; scheduled_for: 2026-04-03T16:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | complete | detail: Single-level home; grab bars installed |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Glucometer teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to the hospital outpatient pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | complete | detail: Hemi-walker training completed with PT |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on stroke warning signs (BE FAST) and secondary prevention completed |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Son to drive patient home; documented_at: 2026-03-23T12:00:00-05:00; window: {'start': '2026-03-24T14:00:00-05:00', 'end': '2026-03-24T15:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and son to review the discharge plan. 3/24 12:45: Son called: car broke down, cannot come today. No alternative ride arranged yet. Discharge paperwork still waiting on the summary.

**nursing_note**

Slept well overnight. Voiding without difficulty. A blood sugar reading was briefly elevated on the morning of day 2. The patient's insulin was adjusted slightly and all subsequent readings have been within the target range.

**physician_note**

77-year-old man with hyperlipidemia, type 2 diabetes, admitted 3/20 with left thalamic infarct with sensory deficits. Deficits stable for 48 hours; passed bedside swallow.

---

## Answer key (generated draft)

**Barriers**

- B-S02 (single-field) — evidence: tracked_fields.transport_status, free_text_notes.case_manager_note
- B-S06 (single-field) — evidence: tracked_fields.discharge_summary_status

**Information gaps**

- none

**Tasks**

- T-CM04 resolves B-S02
- T-MD01 resolves B-S06 — needs sign-off GR-A06 (sign_discharge_summary)

**Must not flag (negative controls):** B-C02
