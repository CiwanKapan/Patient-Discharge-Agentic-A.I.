# CASE-011 — condition CO

**Planned discharge window:** 2026-03-17T11:00:00-05:00 to 2026-03-17T13:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Wife is primary caregiver |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Pulmonology clinic visit booked (first available); scheduled_for: 2026-04-25T10:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete |  |
| medication_availability_status | complete | detail: Discharge prescriptions sent to the hospital outpatient pharmacy |
| medication_education_status | complete |  |
| medication_reconciliation_status | unknown | detail: Not addressed in flowsheet |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | complete | detail: Uses home oxygen 2 L/min at baseline; supply confirmed |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_consult | in_progress | detail: Pulmonary rehabilitation consult requested yesterday; recommendations not yet documented |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Wife to drive patient home; window: {'start': '2026-03-17T11:30:00-05:00', 'end': '2026-03-17T12:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and wife to review the discharge plan. Original evening van slot cancelled; family will drive at the planned discharge time instead.

**nursing_note**

Slept well overnight. Voiding without difficulty. Pulmonary rehabilitation has not seen the patient yet.

**physician_note**

80-year-old man with osteoporosis, former smoker (40 pack-years), admitted 3/10 with COPD exacerbation triggered by viral bronchitis. Weaned from BiPAP on day 2; now on room air at rest. Needs pulmonology clinic follow-up within 14 days of discharge. A slight elevation in liver enzymes was noted on day 1. The test was repeated on day 3 and the result returned to normal. No action is needed.

---

## Answer key (generated draft)

**Barriers**

- B-C04 (single-field) — evidence: tracked_fields.pending_consult

**Information gaps**

- tracked_fields.medication_reconciliation_status → could indicate B-C01

**Tasks**

- T-MD03 resolves B-C04

**Must not flag (negative controls):** B-C01, B-C02, B-S02, B-S07
