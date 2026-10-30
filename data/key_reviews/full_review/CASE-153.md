# CASE-153 — condition ST

**Planned discharge window:** 2026-03-02T15:00:00-05:00 to 2026-03-02T17:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Son will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | in_progress | detail: Dietitian visit for mechanical soft dysphagia diet with thin liquids scheduled but not completed |
| discharge_summary_status | complete |  |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Neurology clinic visit booked; scheduled_for: 2026-03-10T17:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | complete | detail: Single-level home; grab bars installed |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Glucometer teaching done with return demonstration |
| medical_stability_status | complete |  |
| medication_availability_status | complete | detail: Discharge prescriptions sent to CVS |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | complete | detail: Wheelchair training completed with PT |
| outpatient_therapy_status | not_started | detail: Outpatient PT/OT referral not placed |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on stroke warning signs (BE FAST) and secondary prevention completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Neurology signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Son to take patient home; window: {'start': '2026-03-02T15:00:00-05:00', 'end': '2026-03-02T16:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with son.

**nursing_note**

Ambulated in hallway with son present.

**physician_note**

71-year-old man with hyperlipidemia, type 2 diabetes, admitted 2/23 with left thalamic infarct with sensory deficits. NIHSS improved from 6 to 2.

---

## Answer key (generated draft)

**Barriers**

- B-F04 (single-field) — evidence: tracked_fields.outpatient_therapy_status
- B-E04 (single-field) — evidence: tracked_fields.diet_education_status

**Information gaps**

- none

**Tasks**

- T-CM03 resolves B-F04
- T-RN03 resolves B-E04

**Must not flag (negative controls):** none
