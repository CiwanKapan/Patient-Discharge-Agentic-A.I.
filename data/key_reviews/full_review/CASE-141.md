# CASE-141 — condition OR

**Planned discharge window:** 2026-05-11T14:00:00-05:00 to 2026-05-11T16:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Daughter will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Orthopedic surgery clinic visit booked; scheduled_for: 2026-05-15T13:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | complete | detail: Single-level home; grab bars installed |
| insurance_authorization_status | in_progress | detail: Insurance authorization for short-term rehab placement pending |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to the hospital outpatient pharmacy |
| medication_education_status | not_started | detail: No teaching yet on new apixaban 2.5 mg twice daily x35 days |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | complete | detail: Knee scooter training completed with PT |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on hip/knee precautions and DVT warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Daughter will pick patient up before work; window: {'start': '2026-05-11T08:00:00-05:00', 'end': '2026-05-11T09:00:00-05:00'} |
| wound_status | complete | detail: Incision clean, dry and intact |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning.

**nursing_note**

Slept well overnight. Voiding without difficulty. Patient asked what the new apixaban 2.5 mg twice daily x35 days is for; teaching still needed. A standard nursing handover document was prepared on day 3, summarising the patient's stay for any community nursing team that may be involved after discharge. This was sent to the GP as a courtesy note.

**physician_note**

68-year-old woman with type 2 diabetes, hypertension, admitted 5/5 for left total hip arthroplasty. Post-op day 5; working with PT twice daily.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, planned_discharge_window
- B-E01 (single-field) — evidence: tracked_fields.medication_education_status
- B-S04 (single-field) — evidence: tracked_fields.insurance_authorization_status

**Information gaps**

- none

**Tasks**

- T-CM04 resolves B-S07
- T-RN01 resolves B-E01
- T-CM06 resolves B-S04

**Must not flag (negative controls):** B-S06
