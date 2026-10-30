# CASE-144 — condition HF

**Planned discharge window:** 2026-04-06T10:00:00-05:00 to 2026-04-06T12:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete |  |
| case_manager_status | complete |  |
| diet_education_status | not_started | detail: 2 g sodium and 2 L fluid restriction not yet reviewed with patient |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Cardiology clinic visit booked; scheduled_for: 2026-04-11T10:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to a local independent pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on daily weights and heart failure symptom monitoring completed |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Wheelchair van to take patient home; window: {'start': '2026-04-06T10:30:00-05:00', 'end': '2026-04-06T11:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with sister.

**nursing_note**

Ambulated in hallway with sister present.

**physician_note**

53-year-old man with CKD stage 3, atrial fibrillation, admitted 3/31 with acute decompensated heart failure (EF 30%). Diuresed 6 kg with IV furosemide; now euvolemic on oral regimen.

---

## Answer key (generated draft)

**Barriers**

- B-E04 (single-field) — evidence: tracked_fields.diet_education_status

**Information gaps**

- none

**Tasks**

- T-RN03 resolves B-E04

**Must not flag (negative controls):** none
