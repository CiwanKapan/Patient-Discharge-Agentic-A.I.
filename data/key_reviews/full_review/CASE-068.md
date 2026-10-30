# CASE-068 — condition OR

**Planned discharge window:** 2026-03-23T11:00:00-05:00 to 2026-03-23T13:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | unknown | detail: Not addressed in flowsheet |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Orthopedic surgery clinic visit rebooked at patient request; scheduled_for: 2026-04-01T10:00:00-05:00 |
| home_health_referral_status | complete |  |
| home_safety_status | complete |  |
| insurance_authorization_status | complete |  |
| medical_device_education_status | complete | detail: Incision vacuum dressing teaching done with return demonstration |
| medical_stability_status | complete |  |
| medication_availability_status | complete | detail: Discharge prescriptions sent to a local independent pharmacy |
| medication_education_status | not_started | detail: No teaching yet on new celecoxib 200 mg daily x10 days |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | complete | detail: Rolling walker training completed with PT |
| outpatient_therapy_status | complete |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Internal medicine (co-management) signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Medical transport confirmed; window: {'start': '2026-03-23T17:00:00-05:00', 'end': '2026-03-23T18:00:00-05:00'} |
| wound_status | complete |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning. Patient asked what the new celecoxib 200 mg daily x10 days is for; teaching still needed. Patient asked to move the orthopedic surgery clinic appointment; rebooked within 14 days of discharge.

**nursing_note**

Slept well overnight. Voiding without difficulty.

**physician_note**

72-year-old woman with hypertension, hypothyroidism, admitted 3/17 for right hip hemiarthroplasty after femoral neck fracture. Post-op day 5; pain controlled on oral regimen. A venous thromboembolism risk assessment was completed on admission as per standard protocol. The patient received appropriate preventive measures during the stay. These are no longer needed after discharge.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, planned_discharge_window
- B-E01 (single-field) — evidence: tracked_fields.medication_education_status

**Information gaps**

- tracked_fields.caregiver_status → could indicate B-F03

**Tasks**

- T-CM04 resolves B-S07
- T-RN01 resolves B-E01

**Must not flag (negative controls):** B-F01, B-F03
