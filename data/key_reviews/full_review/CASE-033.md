# CASE-033 — condition CO

**Planned discharge window:** 2026-04-06T09:00:00-05:00 to 2026-04-06T11:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete |  |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: PCP visit booked; scheduled_for: 2026-04-15T10:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to Walgreens |
| medication_education_status | complete |  |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | complete | detail: Uses home oxygen 2 L/min at baseline; supply confirmed |
| patient_education_status | complete |  |
| pcp_notification_status | not_started | detail: PCP not yet notified of admission or medication changes |
| pending_consult | complete | detail: Pulmonary rehabilitation signed off |
| pending_imaging | complete |  |
| pending_labs | complete |  |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Nephew to take patient home; window: {'start': '2026-04-06T10:00:00-05:00', 'end': '2026-04-06T11:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and nephew to review the discharge plan.

**nursing_note**

Ambulated in hallway with nephew present.

**physician_note**

57-year-old man with hypertension, former smoker (40 pack-years), admitted 4/1 with AECOPD with hypercapnic respiratory failure, now resolved. Weaned from BiPAP on day 2; now on room air at rest.

---

## Answer key (generated draft)

**Barriers**

- B-F05 (single-field) — evidence: tracked_fields.pcp_notification_status

**Information gaps**

- none

**Tasks**

- T-CM08 resolves B-F05

**Must not flag (negative controls):** none
