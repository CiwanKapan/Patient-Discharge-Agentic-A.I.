# CASE-103 — condition OR

**Planned discharge window:** 2026-06-16T10:00:00-05:00 to 2026-06-16T12:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Sister will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Orthopedic surgery clinic visit booked; scheduled_for: 2026-06-27T09:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | complete | detail: Single-level home; grab bars installed |
| insurance_authorization_status | complete |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete |  |
| medication_education_status | complete |  |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_started | detail: Crutches education not done |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on hip/knee precautions and DVT warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Sister to take patient home; window: {'start': '2026-06-16T11:00:00-05:00', 'end': '2026-06-16T12:00:00-05:00'} |
| wound_status | complete |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with sister.

**nursing_note**

Ambulated in hallway with sister present.

**physician_note**

84-year-old man with hypothyroidism, osteoarthritis, admitted 6/11 for right hip hemiarthroplasty after femoral neck fracture. Post-op day 4; tolerating diet, voiding.

---

## Answer key (generated draft)

**Barriers**

- B-E05 (single-field) — evidence: tracked_fields.mobile_device_education_status

**Information gaps**

- none

**Tasks**

- T-RN07 resolves B-E05

**Must not flag (negative controls):** none
