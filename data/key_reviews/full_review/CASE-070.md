# CASE-070 — condition ST

**Planned discharge window:** 2026-04-20T11:00:00-05:00 to 2026-04-20T13:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete |  |
| case_manager_status | complete |  |
| diet_education_status | complete |  |
| discharge_summary_status | complete |  |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Stroke clinic visit booked; scheduled_for: 2026-04-27T10:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | complete | detail: Single-level home; grab bars installed |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to the hospital outpatient pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | in_progress | detail: Quad cane training started; patient not yet safe on stairs |
| outpatient_therapy_status | not_started | detail: Outpatient PT/OT referral not placed |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on stroke warning signs (BE FAST) and secondary prevention completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Neurology signed off |
| pending_imaging | complete |  |
| pending_labs | complete |  |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Medical transport to take patient home; window: {'start': '2026-04-20T11:30:00-05:00', 'end': '2026-04-20T12:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and nephew to review the discharge plan.

**nursing_note**

Slept well overnight. Voiding without difficulty.

**physician_note**

55-year-old woman with hypertension, atrial fibrillation, admitted 4/13 with right pontine lacunar infarct. NIHSS improved from 6 to 2.

---

## Answer key (generated draft)

**Barriers**

- B-F04 (single-field) — evidence: tracked_fields.outpatient_therapy_status
- B-E05 (single-field) — evidence: tracked_fields.mobile_device_education_status

**Information gaps**

- none

**Tasks**

- T-CM03 resolves B-F04
- T-RN07 resolves B-E05

**Must not flag (negative controls):** none
