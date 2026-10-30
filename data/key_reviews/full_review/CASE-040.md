# CASE-040 — condition CO

**Planned discharge window:** 2026-04-17T13:00:00-05:00 to 2026-04-17T15:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Husband is primary caregiver; works days, available evenings; window: {'start': '2026-04-17T17:00:00-05:00', 'end': '2026-04-17T21:00:00-05:00'} |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete |  |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Pulmonology clinic visit booked; scheduled_for: 2026-04-26T15:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_started | detail: Spacer with new inhaler education not completed |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete |  |
| medication_education_status | complete |  |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | complete |  |
| patient_education_status | complete | detail: Teaching on inhaler technique and the COPD action plan completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Pulmonology signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Husband to drive patient home after work; window: {'start': '2026-04-17T17:30:00-05:00', 'end': '2026-04-17T18:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and husband to review the discharge plan.

**nursing_note**

Ambulated in hallway with husband present.

**physician_note**

74-year-old woman with osteoporosis, hypertension, admitted 4/14 with COPD exacerbation triggered by viral bronchitis. Completed 5 days of systemic steroids; wheeze resolved. A short course of a steroid tablet was used during the admission to reduce inflammation. The course is complete. No steroid has been added to the discharge medication list.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, tracked_fields.caregiver_status, planned_discharge_window
- B-E06 (single-field) — evidence: tracked_fields.medical_device_education_status

**Information gaps**

- none

**Tasks**

- T-CM04 resolves B-S07
- T-RN08 resolves B-E06

**Must not flag (negative controls):** B-C01
