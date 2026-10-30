# CASE-064 — condition ST

**Planned discharge window:** 2026-03-20T13:00:00-05:00 to 2026-03-20T15:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Sister will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | complete |  |
| discharge_summary_status | complete |  |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Stroke clinic visit booked; scheduled_for: 2026-03-25T15:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | in_progress | detail: OT flagged tub shower and no grab bars; modifications not arranged |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Glucometer teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to Walgreens |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | complete | detail: Quad cane training completed with PT |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | in_progress | detail: Fasting lipid panel resulted overnight but not yet reviewed by physician |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Sister to take patient home; window: {'start': '2026-03-20T14:00:00-05:00', 'end': '2026-03-20T15:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning.

**nursing_note**

Ambulated in hallway with sister present.

**physician_note**

83-year-old woman with type 2 diabetes, hyperlipidemia, admitted 3/13 with left thalamic infarct with sensory deficits. NIHSS improved from 6 to 2.

---

## Answer key (generated draft)

**Barriers**

- B-S03 (single-field) — evidence: tracked_fields.home_safety_status
- B-C02 (single-field) — evidence: tracked_fields.pending_labs

**Information gaps**

- none

**Tasks**

- T-CM05 resolves B-S03
- T-MD02 resolves B-C02

**Must not flag (negative controls):** none
