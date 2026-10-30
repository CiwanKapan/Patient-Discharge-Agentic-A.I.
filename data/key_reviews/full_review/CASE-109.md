# CASE-109 — condition PN

**Planned discharge window:** 2026-03-16T12:00:00-05:00 to 2026-03-16T14:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete |  |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete |  |
| financial_status | in_progress | detail: Patient uninsured; financial counselor referral pending |
| followup_appointment_status | complete | detail: Pulmonology clinic visit booked; scheduled_for: 2026-03-20T14:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to Walgreens |
| medication_education_status | in_progress | detail: Teaching on levofloxacin 750 mg daily x3 days started; teach-back not completed |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on completing the antibiotic course and pneumonia warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Speech-language pathology (swallow) signed off |
| pending_imaging | complete |  |
| pending_labs | complete |  |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Wheelchair van booked; window: {'start': '2026-03-17T12:00:00-05:00', 'end': '2026-03-17T13:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with husband. Patient asked what the new levofloxacin 750 mg daily x3 days is for; teaching still needed.

**nursing_note**

Ambulated in hallway with husband present.

**physician_note**

54-year-old woman with asthma, hypertension, admitted 3/11 with multilobar community-acquired pneumonia. Afebrile for 48 hours on IV antibiotics; switched to oral today. The patient reads with glasses. All written discharge materials were provided in large print at the patient's request. The patient confirmed they could read and understand everything.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, planned_discharge_window
- B-E01 (single-field) — evidence: tracked_fields.medication_education_status
- B-S01 (single-field) — evidence: tracked_fields.financial_status

**Information gaps**

- none

**Tasks**

- T-CM04 resolves B-S07
- T-RN01 resolves B-E01
- T-CM07 resolves B-S01

**Must not flag (negative controls):** B-E03
