# CASE-062 — condition PN

**Planned discharge window:** 2026-04-14T12:00:00-05:00 to 2026-04-14T14:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete |  |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: PCP visit booked; scheduled_for: 2026-04-18T12:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_started | detail: Incentive spirometer education not completed |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete |  |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on completing the antibiotic course and pneumonia warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | in_progress | detail: CT chest to exclude empyema completed; awaiting radiology read |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | in_progress | detail: PT evaluation: needs moderate assistance for transfers; not safe to ambulate alone |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Medical transport confirmed; window: {'start': '2026-04-15T12:30:00-05:00', 'end': '2026-04-15T13:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and daughter to review the discharge plan.

**nursing_note**

Ambulated in hallway with daughter present. A routine review of the patient's vaccination history was completed. All recommended vaccinations were up to date and no new vaccinations were needed during this stay.

**physician_note**

79-year-old woman with type 2 diabetes, dementia (mild), admitted 4/8 with aspiration pneumonia, improving. Oxygen weaned to room air yesterday.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, planned_discharge_window
- B-C05 (single-field) — evidence: tracked_fields.physical_function_status
- B-E06 (single-field) — evidence: tracked_fields.medical_device_education_status
- B-C03 (single-field) — evidence: tracked_fields.pending_imaging

**Information gaps**

- none

**Tasks**

- T-CM04 resolves B-S07
- T-RN06 resolves B-C05
- T-RN08 resolves B-E06
- T-MD02 resolves B-C03

**Must not flag (negative controls):** none
