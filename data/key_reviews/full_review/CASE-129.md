# CASE-129 — condition PN

**Planned discharge window:** 2026-04-06T15:00:00-05:00 to 2026-04-06T17:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Son will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Pulmonology clinic visit booked; scheduled_for: 2026-04-10T16:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to a local independent pharmacy |
| medication_education_status | complete |  |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on completing the antibiotic course and pneumonia warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Speech-language pathology (swallow) signed off |
| pending_imaging | in_progress | detail: CT chest to exclude empyema completed; awaiting radiology read |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Medical transport to take patient home; window: {'start': '2026-04-06T15:00:00-05:00', 'end': '2026-04-06T16:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning.

**nursing_note**

Up in chair for meals. Pain controlled.

**physician_note**

61-year-old man with type 2 diabetes, dementia (mild), admitted 3/31 with multilobar community-acquired pneumonia. Afebrile for 48 hours on IV antibiotics; switched to oral today.

---

## Answer key (generated draft)

**Barriers**

- B-C03 (single-field) — evidence: tracked_fields.pending_imaging

**Information gaps**

- none

**Tasks**

- T-MD02 resolves B-C03

**Must not flag (negative controls):** none
