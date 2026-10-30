# CASE-014 — condition HF

**Planned discharge window:** 2026-03-20T11:00:00-05:00 to 2026-03-20T13:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete |  |
| case_manager_status | complete |  |
| diet_education_status | complete |  |
| discharge_summary_status | complete |  |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Cardiology clinic visit booked; scheduled_for: 2026-03-24T13:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | in_progress | detail: Telemonitoring scale teaching started; return demonstration pending |
| medical_stability_status | complete |  |
| medication_availability_status | complete | detail: Discharge prescriptions sent to Walgreens |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Electrophysiology signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Sister to take patient home; window: {'start': '2026-03-20T12:00:00-05:00', 'end': '2026-03-20T13:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and sister to review the discharge plan.

**nursing_note**

Vitals stable this shift. Tolerating diet.

**physician_note**

89-year-old woman with type 2 diabetes, CKD stage 3, admitted 3/16 with acute decompensated heart failure (EF 30%). Transitioned from IV to oral diuretic yesterday; weight stable.

---

## Answer key (generated draft)

**Barriers**

- B-E06 (single-field) — evidence: tracked_fields.medical_device_education_status

**Information gaps**

- none

**Tasks**

- T-RN08 resolves B-E06

**Must not flag (negative controls):** none
