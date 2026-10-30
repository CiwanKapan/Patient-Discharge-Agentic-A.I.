# CASE-106 — condition PN

**Planned discharge window:** 2026-05-05T10:00:00-05:00 to 2026-05-05T12:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Daughter will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete |  |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Pulmonology clinic visit booked; scheduled_for: 2026-05-09T09:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to the hospital outpatient pharmacy |
| medication_education_status | complete |  |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | not_started | detail: PCP not yet notified of admission or medication changes |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Daughter to take patient home; window: {'start': '2026-05-05T10:00:00-05:00', 'end': '2026-05-05T11:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and daughter to review the discharge plan.

**nursing_note**

Up in chair for meals. Pain controlled.

**physician_note**

56-year-old woman with dementia (mild), hypertension, admitted 5/2 with right lower lobe community-acquired pneumonia. Afebrile for 48 hours on IV antibiotics; switched to oral today.

---

## Answer key (generated draft)

**Barriers**

- B-F05 (single-field) — evidence: tracked_fields.pcp_notification_status

**Information gaps**

- none

**Tasks**

- T-CM08 resolves B-F05

**Must not flag (negative controls):** none
