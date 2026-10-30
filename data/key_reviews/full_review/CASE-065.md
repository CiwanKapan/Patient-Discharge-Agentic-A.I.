# CASE-065 — condition OR

**Planned discharge window:** 2026-04-13T08:00:00-05:00 to 2026-04-13T10:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Wife will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete |  |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Orthopedic surgery clinic visit booked; scheduled_for: 2026-04-22T08:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | complete | detail: Single-level home; grab bars installed |
| insurance_authorization_status | complete | detail: DME authorized by insurer |
| medical_device_education_status | complete | detail: Continuous passive motion machine teaching done with return demonstration |
| medical_stability_status | complete |  |
| medication_availability_status | complete |  |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | complete | detail: Crutches training completed with PT |
| outpatient_therapy_status | complete |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on hip/knee precautions and DVT warning signs completed |
| pcp_notification_status | not_started | detail: PCP not yet notified of admission or medication changes |
| pending_consult | complete | detail: Wound care signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Wheelchair van to take patient home; window: {'start': '2026-04-13T09:00:00-05:00', 'end': '2026-04-13T10:00:00-05:00'} |
| wound_status | in_progress | detail: Surgical site pain 7/10 despite oral regimen; not yet controlled |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning.

**nursing_note**

Ambulated in hallway with wife present.

**physician_note**

52-year-old man with hypothyroidism, type 2 diabetes, admitted 4/9 for right hip hemiarthroplasty after femoral neck fracture. Post-op day 3; working with PT twice daily.

---

## Answer key (generated draft)

**Barriers**

- B-C06 (single-field) — evidence: tracked_fields.wound_status
- B-F05 (single-field) — evidence: tracked_fields.pcp_notification_status

**Information gaps**

- none

**Tasks**

- T-RN05 resolves B-C06
- T-CM08 resolves B-F05

**Must not flag (negative controls):** none
