# CASE-035 — condition OR

**Planned discharge window:** 2026-06-29T15:00:00-05:00 to 2026-06-29T17:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete |  |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Orthopedic surgery clinic visit booked; scheduled_for: 2026-07-13T17:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | complete |  |
| insurance_authorization_status | complete | detail: DME authorized by insurer |
| medical_device_education_status | complete | detail: Incision vacuum dressing teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to a local independent pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | complete |  |
| outpatient_therapy_status | complete |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on hip/knee precautions and DVT warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Physical medicine and rehabilitation signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Husband to take patient home; window: {'start': '2026-06-29T16:00:00-05:00', 'end': '2026-06-29T17:00:00-05:00'} |
| wound_status | in_progress | detail: Incision with new serous drainage and surrounding erythema; wound team to reassess |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and husband to review the discharge plan.

**nursing_note**

Up in chair for meals. Pain controlled.

**physician_note**

64-year-old woman with type 2 diabetes, obesity, admitted 6/26 for right hip hemiarthroplasty after femoral neck fracture. Post-op day 2; pain controlled on oral regimen.

---

## Answer key (generated draft)

**Barriers**

- B-C06 (single-field) — evidence: tracked_fields.wound_status

**Information gaps**

- none

**Tasks**

- T-RN05 resolves B-C06

**Must not flag (negative controls):** none
