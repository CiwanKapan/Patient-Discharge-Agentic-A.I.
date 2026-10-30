# CASE-066 — condition OR

**Planned discharge window:** 2026-03-30T13:00:00-05:00 to 2026-03-30T15:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Son will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Orthopedic surgery clinic visit booked; scheduled_for: 2026-04-13T12:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | complete |  |
| insurance_authorization_status | in_progress | detail: Insurance authorization for short-term rehab placement pending |
| medical_device_education_status | complete | detail: Continuous passive motion machine teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to CVS |
| medication_education_status | complete |  |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | complete | detail: Rolling walker training completed with PT |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Internal medicine (co-management) signed off |
| pending_imaging | complete |  |
| pending_labs | complete |  |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Son to take patient home; window: {'start': '2026-03-30T13:30:00-05:00', 'end': '2026-03-30T14:30:00-05:00'} |
| wound_status | complete |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with son.

**nursing_note**

Up in chair for meals. Pain controlled.

**physician_note**

62-year-old woman with obesity, type 2 diabetes, admitted 3/25 for ORIF of right bimalleolar ankle fracture. Post-op day 4; pain controlled on oral regimen.

---

## Answer key (generated draft)

**Barriers**

- B-S04 (single-field) — evidence: tracked_fields.insurance_authorization_status

**Information gaps**

- none

**Tasks**

- T-CM06 resolves B-S04

**Must not flag (negative controls):** none
