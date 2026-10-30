# CASE-099 — condition HF

**Planned discharge window:** 2026-04-21T15:00:00-05:00 to 2026-04-21T17:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Sister will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_started | detail: 2 g sodium and 2 L fluid restriction not yet reviewed with patient |
| discharge_summary_status | complete |  |
| financial_status | complete |  |
| followup_appointment_status | not_started | detail: Cardiology clinic follow-up not yet booked |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Home scale and blood pressure cuff teaching done with return demonstration |
| medical_stability_status | complete |  |
| medication_availability_status | complete | detail: Discharge prescriptions sent to Walgreens |
| medication_education_status | complete |  |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Wheelchair van to take patient home; window: {'start': '2026-04-21T15:00:00-05:00', 'end': '2026-04-21T16:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning.

**nursing_note**

Slept well overnight. Voiding without difficulty.

**physician_note**

57-year-old woman with CAD s/p PCI, type 2 diabetes, admitted 4/16 with acute on chronic HFrEF exacerbation with volume overload. Transitioned from IV to oral diuretic yesterday; weight stable.

---

## Answer key (generated draft)

**Barriers**

- B-F01 (single-field) — evidence: tracked_fields.followup_appointment_status
- B-E04 (single-field) — evidence: tracked_fields.diet_education_status

**Information gaps**

- none

**Tasks**

- T-CM01 resolves B-F01
- T-RN03 resolves B-E04

**Must not flag (negative controls):** none
