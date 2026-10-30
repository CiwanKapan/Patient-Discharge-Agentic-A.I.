# CASE-115 — condition PN

**Planned discharge window:** 2026-05-07T12:00:00-05:00 to 2026-05-07T14:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Son will stay with patient for the first week |
| case_manager_status | in_progress | detail: Assigned case manager out sick; coverage not confirmed |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete |  |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: PCP visit booked; scheduled_for: 2026-05-11T11:00:00-05:00 |
| home_health_referral_status | complete |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | in_progress | detail: Incentive spirometer teaching started; return demonstration pending |
| medical_stability_status | complete |  |
| medication_availability_status | complete | detail: Discharge prescriptions sent to a local independent pharmacy |
| medication_education_status | complete |  |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Pulmonology signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Son to take patient home; window: {'start': '2026-05-07T12:30:00-05:00', 'end': '2026-05-07T13:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and son to review the discharge plan.

**nursing_note**

Ambulated in hallway with son present.

**physician_note**

66-year-old man with asthma, dementia (mild), admitted 4/30 with multilobar community-acquired pneumonia. Leukocytosis resolved; tolerating diet.

---

## Answer key (generated draft)

**Barriers**

- B-S05 (single-field) — evidence: tracked_fields.case_manager_status
- B-E06 (single-field) — evidence: tracked_fields.medical_device_education_status

**Information gaps**

- none

**Tasks**

- T-CM09 resolves B-S05
- T-RN08 resolves B-E06

**Must not flag (negative controls):** none
