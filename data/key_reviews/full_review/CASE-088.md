# CASE-088 — condition CO

**Planned discharge window:** 2026-05-25T12:00:00-05:00 to 2026-05-25T14:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Son will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Pulmonology clinic visit booked; scheduled_for: 2026-05-29T12:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to Walgreens |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | complete | detail: Uses home oxygen 2 L/min at baseline; supply confirmed |
| patient_education_status | complete |  |
| pcp_notification_status | not_started | detail: PCP not yet notified of admission or medication changes |
| pending_consult | in_progress | detail: Palliative care consult requested yesterday; recommendations not yet documented |
| pending_imaging | complete |  |
| pending_labs | complete |  |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Son to take patient home; window: {'start': '2026-05-25T13:00:00-05:00', 'end': '2026-05-25T14:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and son to review the discharge plan.

**nursing_note**

Slept well overnight. Voiding without difficulty.

**physician_note**

88-year-old woman with GERD, former smoker (40 pack-years), admitted 5/19 with COPD exacerbation triggered by viral bronchitis. Weaned from BiPAP on day 2; now on room air at rest.

---

## Answer key (generated draft)

**Barriers**

- B-C04 (single-field) — evidence: tracked_fields.pending_consult
- B-F05 (single-field) — evidence: tracked_fields.pcp_notification_status

**Information gaps**

- none

**Tasks**

- T-MD03 resolves B-C04
- T-CM08 resolves B-F05

**Must not flag (negative controls):** none
