# CASE-131 — condition HF

**Planned discharge window:** 2026-03-30T13:00:00-05:00 to 2026-03-30T15:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete |  |
| case_manager_status | complete |  |
| diet_education_status | not_started | detail: 2 g sodium and 2 L fluid restriction not yet reviewed with patient |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: PCP visit booked; scheduled_for: 2026-04-06T12:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete |  |
| medication_availability_status | complete | detail: Discharge prescriptions sent to Walgreens |
| medication_reconciliation_status | in_progress | detail: Discrepancy between home and inpatient metoprolol succinate doses not yet resolved |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on daily weights and heart failure symptom monitoring completed |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete |  |
| physical_function_status | not_started | detail: Functional assessment not done; patient deconditioned after 5-day stay |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Nephew will pick patient up before work; window: {'start': '2026-03-30T09:00:00-05:00', 'end': '2026-03-30T10:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning.

**nursing_note**

Vitals stable this shift. Tolerating diet. PT recommends assistance with all transfers for now.

**physician_note**

89-year-old woman with CKD stage 3, type 2 diabetes, admitted 3/25 with new-onset heart failure with reduced ejection fraction. Net negative 3.1 L this admission; dyspnea back to baseline. The patient already has a home blood pressure monitor and has been using it correctly for several months. No new equipment or education was needed for self-monitoring.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, planned_discharge_window
- B-E04 (single-field) — evidence: tracked_fields.diet_education_status
- B-C05 (single-field) — evidence: tracked_fields.physical_function_status
- B-C01 (single-field) — evidence: tracked_fields.medication_reconciliation_status

**Information gaps**

- tracked_fields.medication_education_status → could indicate B-E01

**Tasks**

- T-CM04 resolves B-S07
- T-RN03 resolves B-E04
- T-RN06 resolves B-C05
- T-PH01 resolves B-C01 — needs sign-off GR-A02 (modify_medication_list)

**Must not flag (negative controls):** B-E01, B-E06
