# CASE-146 — condition HF

**Planned discharge window:** 2026-05-27T09:00:00-05:00 to 2026-05-27T11:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Nephew will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | complete |  |
| discharge_summary_status | in_progress | detail: Discharge summary drafted; not signed |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Heart failure clinic visit booked; scheduled_for: 2026-05-30T09:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to Walgreens |
| medication_education_status | complete |  |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete |  |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Medical transport to take patient home; window: {'start': '2026-05-27T09:00:00-05:00', 'end': '2026-05-27T10:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with nephew.

**nursing_note**

Slept well overnight. Voiding without difficulty.

**physician_note**

72-year-old man with hypertension, atrial fibrillation, admitted 5/20 with acute on chronic HFrEF exacerbation with volume overload. Diuresed 6 kg with IV furosemide; now euvolemic on oral regimen.

---

## Answer key (generated draft)

**Barriers**

- B-S06 (single-field) — evidence: tracked_fields.discharge_summary_status

**Information gaps**

- none

**Tasks**

- T-MD01 resolves B-S06 — needs sign-off GR-A06 (sign_discharge_summary)

**Must not flag (negative controls):** none
