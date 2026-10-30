# CASE-120 — condition OR

**Planned discharge window:** 2026-06-18T11:00:00-05:00 to 2026-06-18T13:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete |  |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete |  |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Orthopedic surgery clinic visit booked; scheduled_for: 2026-06-30T13:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | complete | detail: Single-level home; grab bars installed |
| insurance_authorization_status | complete | detail: DME authorized by insurer |
| medical_device_education_status | complete | detail: Incision vacuum dressing teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete |  |
| medication_education_status | in_progress | detail: Teaching on celecoxib 200 mg daily x10 days started; teach-back not completed |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | complete | detail: Knee scooter training completed with PT |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on hip/knee precautions and DVT warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Physical medicine and rehabilitation signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Son to drive patient home; documented_at: 2026-06-17T09:00:00-05:00; window: {'start': '2026-06-18T11:00:00-05:00', 'end': '2026-06-18T12:00:00-05:00'} |
| wound_status | complete | detail: Incision clean, dry and intact |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with son. 6/18 08:20: Son tested positive for COVID and cannot pick the patient up. Patient does not drive; no other ride identified. Patient asked what the new celecoxib 200 mg daily x10 days is for; teaching still needed.

**nursing_note**

Up in chair for meals. Pain controlled. The patient had a cataract removed from one eye two years ago. The result was successful. Vision in both eyes is stable and this has no current clinical significance.

**physician_note**

70-year-old woman with hypothyroidism, obesity, admitted 6/13 for elective right total knee arthroplasty. Post-op day 4; pain controlled on oral regimen.

---

## Answer key (generated draft)

**Barriers**

- B-S02 (single-field) — evidence: tracked_fields.transport_status, free_text_notes.case_manager_note
- B-E01 (single-field) — evidence: tracked_fields.medication_education_status

**Information gaps**

- none

**Tasks**

- T-CM04 resolves B-S02
- T-RN01 resolves B-E01

**Must not flag (negative controls):** none
