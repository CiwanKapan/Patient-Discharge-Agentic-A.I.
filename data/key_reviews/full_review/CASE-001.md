# CASE-001 — condition PN

**Planned discharge window:** 2026-04-23T14:00:00-05:00 to 2026-04-23T16:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete |  |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | in_progress | detail: Discharge summary drafted; not signed |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: PCP visit booked; scheduled_for: 2026-04-28T15:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Incentive spirometer teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to CVS |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Pulmonology signed off |
| pending_imaging | in_progress | detail: CT chest to exclude empyema completed; awaiting radiology read |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Son to take patient home; window: {'start': '2026-04-23T14:30:00-05:00', 'end': '2026-04-23T15:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and son to review the discharge plan.

**nursing_note**

Vitals stable this shift. Tolerating diet.

**physician_note**

71-year-old woman with dementia (mild), hypertension, admitted 4/19 with right lower lobe community-acquired pneumonia. Oxygen weaned to room air yesterday.

---

## Answer key (generated draft)

**Barriers**

- B-S06 (single-field) — evidence: tracked_fields.discharge_summary_status
- B-C03 (single-field) — evidence: tracked_fields.pending_imaging

**Information gaps**

- none

**Tasks**

- T-MD01 resolves B-S06 — needs sign-off GR-A06 (sign_discharge_summary)
- T-MD02 resolves B-C03

**Must not flag (negative controls):** none
