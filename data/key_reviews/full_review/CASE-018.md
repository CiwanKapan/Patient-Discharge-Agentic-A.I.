# CASE-018 — condition OR

**Planned discharge window:** 2026-03-13T12:00:00-05:00 to 2026-03-13T14:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Son will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | not_started | detail: Orthopedic surgery clinic follow-up not yet booked |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | complete | detail: Single-level home; grab bars installed |
| insurance_authorization_status | complete | detail: DME authorized by insurer |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete |  |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | complete | detail: Crutches training completed with PT |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on hip/knee precautions and DVT warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Son to take patient home; window: {'start': '2026-03-13T12:00:00-05:00', 'end': '2026-03-13T13:00:00-05:00'} |
| wound_status | complete | detail: Incision clean, dry and intact |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and son to review the discharge plan.

**nursing_note**

Vitals stable this shift. Tolerating diet.

**physician_note**

74-year-old woman with osteoarthritis, obesity, admitted 3/7 for elective right total knee arthroplasty. Post-op day 5; tolerating diet, voiding.

---

## Answer key (generated draft)

**Barriers**

- B-F01 (single-field) — evidence: tracked_fields.followup_appointment_status

**Information gaps**

- none

**Tasks**

- T-CM01 resolves B-F01

**Must not flag (negative controls):** none
