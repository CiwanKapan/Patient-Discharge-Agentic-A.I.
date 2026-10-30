# CASE-082 — condition OR

**Planned discharge window:** 2026-04-08T09:00:00-05:00 to 2026-04-08T11:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Sister will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete |  |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Orthopedic surgery clinic visit booked; scheduled_for: 2026-04-15T08:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | complete | detail: Single-level home; grab bars installed |
| insurance_authorization_status | complete | detail: DME authorized by insurer |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to the hospital outpatient pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | complete |  |
| outpatient_therapy_status | not_started | detail: Outpatient PT/OT referral not placed |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Physical medicine and rehabilitation signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Wheelchair van to take patient home; window: {'start': '2026-04-08T10:00:00-05:00', 'end': '2026-04-08T11:00:00-05:00'} |
| wound_status | complete | detail: Incision clean, dry and intact |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning.

**nursing_note**

Slept well overnight. Voiding without difficulty.

**physician_note**

82-year-old woman with hypothyroidism, type 2 diabetes, admitted 4/5 for ORIF of right bimalleolar ankle fracture. Post-op day 2; pain controlled on oral regimen.

---

## Answer key (generated draft)

**Barriers**

- B-F04 (single-field) — evidence: tracked_fields.outpatient_therapy_status

**Information gaps**

- none

**Tasks**

- T-CM03 resolves B-F04

**Must not flag (negative controls):** none
