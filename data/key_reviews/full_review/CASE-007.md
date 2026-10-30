# CASE-007 — condition ST

**Planned discharge window:** 2026-03-30T08:00:00-05:00 to 2026-03-30T10:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Nephew will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | complete | detail: mechanical soft dysphagia diet with thin liquids reviewed with teach-back |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Stroke clinic visit booked (first available); scheduled_for: 2026-05-13T14:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | complete |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete |  |
| medication_availability_status | complete |  |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | unknown | detail: Not documented |
| mobile_device_education_status | not_started | detail: Hemi-walker education not done |
| outpatient_therapy_status | complete |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on stroke warning signs (BE FAST) and secondary prevention completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Neurology signed off |
| pending_imaging | complete |  |
| pending_labs | in_progress | detail: HbA1c resulted overnight but not yet reviewed by physician |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Nephew to take patient home; window: {'start': '2026-03-30T08:00:00-05:00', 'end': '2026-03-30T09:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and nephew to review the discharge plan. Physician to review the HbA1c before discharge.

**nursing_note**

Up in chair for meals. Pain controlled.

**physician_note**

60-year-old man with prior TIA, atrial fibrillation, admitted 3/24 with left thalamic infarct with sensory deficits. Deficits stable for 48 hours; passed bedside swallow. Needs stroke clinic follow-up within 14 days of discharge. A mild rash appeared briefly at the IV insertion site on day 2. It was assessed as a minor irritation, treated with a topical cream, and has fully resolved.

---

## Answer key (generated draft)

**Barriers**

- B-E05 (single-field) — evidence: tracked_fields.mobile_device_education_status
- B-C02 (single-field) — evidence: tracked_fields.pending_labs

**Information gaps**

- tracked_fields.medication_reconciliation_status → could indicate B-C01

**Tasks**

- T-RN07 resolves B-E05
- T-MD02 resolves B-C02

**Must not flag (negative controls):** B-C01
