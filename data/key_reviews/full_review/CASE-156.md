# CASE-156 — condition PN

**Planned discharge window:** 2026-03-30T14:00:00-05:00 to 2026-03-30T16:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete |  |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Pulmonology clinic visit booked; scheduled_for: 2026-04-02T13:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | in_progress | detail: Discharge prescriptions not yet sent; CVS does not stock amoxicillin-clavulanate 875/125 mg twice daily x5 days |
| medication_education_status | complete |  |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on completing the antibiotic course and pneumonia warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Speech-language pathology (swallow) signed off |
| pending_imaging | in_progress | detail: CT chest to exclude empyema completed; awaiting radiology read |
| pending_labs | complete |  |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Wife to take patient home; window: {'start': '2026-03-30T14:00:00-05:00', 'end': '2026-03-30T15:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning.

**nursing_note**

Slept well overnight. Voiding without difficulty.

**physician_note**

59-year-old man with dementia (mild), asthma, admitted 3/25 with aspiration pneumonia, improving. Afebrile for 48 hours on IV antibiotics; switched to oral today.

---

## Answer key (generated draft)

**Barriers**

- B-C03 (single-field) — evidence: tracked_fields.pending_imaging
- B-E02 (single-field) — evidence: tracked_fields.medication_availability_status

**Information gaps**

- none

**Tasks**

- T-MD02 resolves B-C03
- T-PH02 resolves B-E02 — needs sign-off GR-A03 (send_prescription)

**Must not flag (negative controls):** none
