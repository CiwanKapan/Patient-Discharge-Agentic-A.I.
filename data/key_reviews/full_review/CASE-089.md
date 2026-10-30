# CASE-089 — condition CO

**Planned discharge window:** 2026-04-03T11:00:00-05:00 to 2026-04-03T13:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Son will stay with patient for the first week |
| case_manager_status | not_started | detail: No case manager assigned to the unit this weekend |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: PCP visit booked; scheduled_for: 2026-04-09T11:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to CVS |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete |  |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Wheelchair van to take patient home; window: {'start': '2026-04-03T12:00:00-05:00', 'end': '2026-04-03T13:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning.

**nursing_note**

Vitals stable this shift. Tolerating diet.

**physician_note**

89-year-old man with anxiety, osteoporosis, admitted 3/31 with acute exacerbation of COPD. Completed 5 days of systemic steroids; wheeze resolved.

---

## Answer key (generated draft)

**Barriers**

- B-S05 (single-field) — evidence: tracked_fields.case_manager_status

**Information gaps**

- none

**Tasks**

- T-CM09 resolves B-S05

**Must not flag (negative controls):** none
