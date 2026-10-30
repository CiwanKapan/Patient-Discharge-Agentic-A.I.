# CASE-071 — condition OR

**Planned discharge window:** 2026-05-26T09:00:00-05:00 to 2026-05-26T11:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Son will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete |  |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Orthopedic surgery clinic visit booked; scheduled_for: 2026-05-29T10:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | complete | detail: Single-level home; grab bars installed |
| insurance_authorization_status | in_progress | detail: Insurance authorization for short-term rehab placement pending |
| medical_device_education_status | complete |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to CVS |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | complete | detail: Rolling walker training completed with PT |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on hip/knee precautions and DVT warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Wound care signed off |
| pending_imaging | complete |  |
| pending_labs | complete |  |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Medical transport to take patient home; window: {'start': '2026-05-26T09:30:00-05:00', 'end': '2026-05-26T10:30:00-05:00'} |
| wound_status | in_progress | detail: Surgical site pain 7/10 despite oral regimen; not yet controlled |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with son.

**nursing_note**

Slept well overnight. Voiding without difficulty.

**physician_note**

66-year-old man with hypothyroidism, hypertension, admitted 5/20 for elective right total knee arthroplasty. Post-op day 5; pain controlled on oral regimen.

---

## Answer key (generated draft)

**Barriers**

- B-C06 (single-field) — evidence: tracked_fields.wound_status
- B-S04 (single-field) — evidence: tracked_fields.insurance_authorization_status

**Information gaps**

- none

**Tasks**

- T-RN05 resolves B-C06
- T-CM06 resolves B-S04

**Must not flag (negative controls):** none
