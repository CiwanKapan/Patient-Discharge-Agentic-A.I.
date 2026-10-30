# CASE-055 — condition CO

**Planned discharge window:** 2026-03-05T11:00:00-05:00 to 2026-03-05T13:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Son will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | not_started | detail: Patient reports she cannot afford the azithromycin copay; no assistance arranged |
| followup_appointment_status | complete | detail: Pulmonology clinic visit booked; scheduled_for: 2026-03-13T10:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to a local independent pharmacy |
| medication_education_status | complete |  |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | complete | detail: Uses home oxygen 2 L/min at baseline; supply confirmed |
| patient_education_status | complete | detail: Teaching on inhaler technique and the COPD action plan completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Palliative care signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Wheelchair van to take patient home; window: {'start': '2026-03-05T12:00:00-05:00', 'end': '2026-03-05T13:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with son.

**nursing_note**

Slept well overnight. Voiding without difficulty.

**physician_note**

84-year-old woman with anxiety, former smoker (40 pack-years), admitted 3/1 with acute exacerbation of COPD. Weaned from BiPAP on day 2; now on room air at rest.

---

## Answer key (generated draft)

**Barriers**

- B-S01 (single-field) — evidence: tracked_fields.financial_status

**Information gaps**

- none

**Tasks**

- T-CM07 resolves B-S01

**Must not flag (negative controls):** none
