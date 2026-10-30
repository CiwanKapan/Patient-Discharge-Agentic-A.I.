# CASE-032 — condition PN

**Planned discharge window:** 2026-05-25T14:00:00-05:00 to 2026-05-25T16:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Wife is primary caregiver |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | in_progress | detail: Discharge summary about 60% complete |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: PCP visit booked (first available); scheduled_for: 2026-06-28T13:00:00-05:00 |
| home_health_referral_status | complete |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to the hospital outpatient pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list, including the dose change; documented_at: 2026-05-24T15:00:00-05:00 |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on completing the antibiotic course and pneumonia warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Pulmonology signed off |
| pending_imaging | in_progress | detail: CT chest to exclude empyema completed; awaiting radiology read |
| pending_labs | complete |  |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Wife to drive patient home; window: {'start': '2026-05-25T14:30:00-05:00', 'end': '2026-05-25T15:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and wife to review the discharge plan. Wife normally works days but has taken the afternoon off to drive the patient home at the planned time. Summary is basically finished. Please sign it on the attending's behalf so the discharge packet can print.

**nursing_note**

Up in chair for meals. Pain controlled. Radiology read on the CT chest to exclude empyema still pending. Discharge paperwork still waiting on the summary. 5/24 15:00: Metformin held until follow-up (was 1000 mg twice daily) this morning. Reviewed with patient and wife at 15:00; teach-back correct.

**physician_note**

64-year-old man with type 2 diabetes, alcohol use disorder in remission, admitted 5/18 with multilobar community-acquired pneumonia. Oxygen weaned to room air yesterday. Needs PCP follow-up within 7 days of discharge. The patient had a hernia repaired surgically four years ago. The repair was successful and the patient has had no recurrence. This is not relevant to the current discharge plan.

---

## Answer key (generated draft)

**Barriers**

- B-C03 (single-field) — evidence: tracked_fields.pending_imaging
- B-S06 (single-field) — evidence: tracked_fields.discharge_summary_status

**Information gaps**

- none

**Tasks**

- T-MD02 resolves B-C03
- T-MD01 resolves B-S06 — needs sign-off GR-A06 (sign_discharge_summary)

**Must not flag (negative controls):** B-E01, B-E07, B-S02, B-S07
