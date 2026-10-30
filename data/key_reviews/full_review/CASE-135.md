# CASE-135 — condition ST

**Planned discharge window:** 2026-03-20T10:00:00-05:00 to 2026-03-20T12:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete |  |
| case_manager_status | complete |  |
| diet_education_status | complete |  |
| discharge_summary_status | complete |  |
| financial_status | in_progress | detail: Patient uninsured; financial counselor referral pending |
| followup_appointment_status | complete | detail: Neurology clinic visit booked; scheduled_for: 2026-03-27T12:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | in_progress | detail: OT flagged tub shower and no grab bars; modifications not arranged |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Home blood pressure monitor teaching done with return demonstration |
| medical_stability_status | complete |  |
| medication_availability_status | complete | detail: Discharge prescriptions sent to CVS |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | complete | detail: Wheelchair training completed with PT |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on stroke warning signs (BE FAST) and secondary prevention completed |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete |  |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Nephew will pick patient up; window: {'start': '2026-03-20T17:00:00-05:00', 'end': '2026-03-20T18:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with nephew. Patient worried about the cost of the new medication. Bedroom is upstairs at home; setup not reviewed yet.

**nursing_note**

Slept well overnight. Voiding without difficulty.

**physician_note**

83-year-old man with hypertension, prior TIA, admitted 3/16 with left MCA ischemic stroke with mild right hemiparesis. NIHSS improved from 6 to 2. The patient's blood pressure has been consistently controlled throughout the stay with no additional medications needed. The neurologist confirmed this is satisfactory for discharge.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, planned_discharge_window
- B-S01 (single-field) — evidence: tracked_fields.financial_status
- B-S03 (single-field) — evidence: tracked_fields.home_safety_status

**Information gaps**

- none

**Tasks**

- T-CM04 resolves B-S07
- T-CM07 resolves B-S01
- T-CM05 resolves B-S03

**Must not flag (negative controls):** B-C07
