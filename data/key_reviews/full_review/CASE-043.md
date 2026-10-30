# CASE-043 — condition CO

**Planned discharge window:** 2026-03-23T15:00:00-05:00 to 2026-03-23T17:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Husband will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: PCP visit booked; scheduled_for: 2026-04-05T16:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Spacer with new inhaler teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to the hospital outpatient pharmacy |
| medication_education_status | in_progress | detail: Teaching on tiotropium 18 mcg inhaled daily started; teach-back not completed |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | complete | detail: Uses home oxygen 2 L/min at baseline; supply confirmed |
| patient_education_status | complete | detail: Teaching on inhaler technique and the COPD action plan completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Palliative care signed off |
| pending_imaging | complete |  |
| pending_labs | complete |  |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Husband to take patient home; window: {'start': '2026-03-23T15:30:00-05:00', 'end': '2026-03-23T16:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning.

**nursing_note**

Slept well overnight. Voiding without difficulty.

**physician_note**

62-year-old woman with GERD, osteoporosis, admitted 3/20 with acute exacerbation of COPD. Completed 5 days of systemic steroids; wheeze resolved.

---

## Answer key (generated draft)

**Barriers**

- B-E01 (single-field) — evidence: tracked_fields.medication_education_status

**Information gaps**

- none

**Tasks**

- T-RN01 resolves B-E01

**Must not flag (negative controls):** none
