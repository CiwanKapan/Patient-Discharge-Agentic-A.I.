# CASE-063 — condition PN

**Planned discharge window:** 2026-04-20T14:00:00-05:00 to 2026-04-20T16:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete |  |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Pulmonology clinic visit booked; scheduled_for: 2026-04-24T13:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | not_started | detail: Amoxicillin-clavulanate 875/125 mg twice daily x5 days needs prior authorization; not available at a local independent pharmacy |
| medication_education_status | complete |  |
| medication_reconciliation_status | not_started | detail: Discharge medication reconciliation not yet done |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on completing the antibiotic course and pneumonia warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Speech-language pathology (swallow) signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Nephew to take patient home; window: {'start': '2026-04-20T14:00:00-05:00', 'end': '2026-04-20T15:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and nephew to review the discharge plan.

**nursing_note**

Ambulated in hallway with nephew present.

**physician_note**

68-year-old man with alcohol use disorder in remission, asthma, admitted 4/14 with right lower lobe community-acquired pneumonia. Oxygen weaned to room air yesterday.

---

## Answer key (generated draft)

**Barriers**

- B-C01 (single-field) — evidence: tracked_fields.medication_reconciliation_status
- B-E02 (single-field) — evidence: tracked_fields.medication_availability_status

**Information gaps**

- none

**Tasks**

- T-PH01 resolves B-C01 — needs sign-off GR-A02 (modify_medication_list)
- T-PH03 resolves B-E02

**Must not flag (negative controls):** none
