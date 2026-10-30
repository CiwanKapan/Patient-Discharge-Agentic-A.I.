# CASE-023 — condition ST

**Planned discharge window:** 2026-04-22T15:00:00-05:00 to 2026-04-22T17:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete |  |
| case_manager_status | complete |  |
| diet_education_status | in_progress | detail: Dietitian visit for mechanical soft dysphagia diet with thin liquids scheduled but not completed |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Stroke clinic visit booked; scheduled_for: 2026-05-06T17:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | complete |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete |  |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_started | detail: Wheelchair education not done |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on stroke warning signs (BE FAST) and secondary prevention completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Neurology signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Sister to take patient home; window: {'start': '2026-04-22T15:30:00-05:00', 'end': '2026-04-22T16:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and sister to review the discharge plan.

**nursing_note**

Ambulated in hallway with sister present.

**physician_note**

53-year-old woman with prior TIA, type 2 diabetes, admitted 4/17 with small right cerebellar infarct. MRI confirmed small infarct; no hemorrhagic conversion.

---

## Answer key (generated draft)

**Barriers**

- B-E04 (single-field) — evidence: tracked_fields.diet_education_status
- B-E05 (single-field) — evidence: tracked_fields.mobile_device_education_status

**Information gaps**

- none

**Tasks**

- T-RN03 resolves B-E04
- T-RN07 resolves B-E05

**Must not flag (negative controls):** none
