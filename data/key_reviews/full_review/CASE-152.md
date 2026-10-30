# CASE-152 — condition HF

**Planned discharge window:** 2026-05-18T08:00:00-05:00 to 2026-05-18T10:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | not_started | detail: No caregiver identified; patient lives alone and needs help with ADLs |
| case_manager_status | complete |  |
| diet_education_status | complete |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Heart failure clinic visit booked; scheduled_for: 2026-05-23T09:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to the hospital outpatient pharmacy |
| medication_education_status | complete |  |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Electrophysiology signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Wheelchair van to take patient home; window: {'start': '2026-05-18T09:00:00-05:00', 'end': '2026-05-18T10:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Discharge planning in progress; CM following daily.

**nursing_note**

Up in chair for meals. Pain controlled.

**physician_note**

86-year-old man with atrial fibrillation, type 2 diabetes, admitted 5/11 with acute on chronic HFrEF exacerbation with volume overload. Diuresed 4 kg with IV furosemide; now euvolemic on oral regimen.

---

## Answer key (generated draft)

**Barriers**

- B-F03 (single-field) — evidence: tracked_fields.caregiver_status

**Information gaps**

- none

**Tasks**

- T-CM02 resolves B-F03

**Must not flag (negative controls):** none
