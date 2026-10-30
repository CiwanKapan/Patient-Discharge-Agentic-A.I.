# CASE-028 — condition CO

**Planned discharge window:** 2026-05-04T12:00:00-05:00 to 2026-05-04T14:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Son will stay with patient for the first two weeks; documented_at: 2026-05-03T10:00:00-05:00 |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete |  |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Pulmonology clinic visit booked; scheduled_for: 2026-05-12T14:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | in_progress | detail: Spacer with new inhaler teaching started; return demonstration pending |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete |  |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | not_started | detail: Discharge medication reconciliation not yet done |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | complete | detail: Uses home oxygen 2 L/min at baseline; supply confirmed |
| patient_education_status | complete | detail: Teaching on inhaler technique and the COPD action plan completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Pulmonology signed off |
| pending_imaging | in_progress | detail: CT chest for nodule follow-up completed; awaiting radiology read |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Wheelchair van to take patient home; window: {'start': '2026-05-04T13:00:00-05:00', 'end': '2026-05-04T14:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Discharge planning in progress; CM following daily. 5/4 10:45: Son called: has to travel for a family emergency tonight and cannot stay with the patient. No other family available.

**nursing_note**

Ambulated in hallway with son present. Radiology read on the CT chest for nodule follow-up still pending. The patient mentioned they have a COPD action plan at home that was written by their GP. They confirmed they are familiar with it and know when to seek help.

**physician_note**

53-year-old woman with osteoporosis, former smoker (40 pack-years), admitted 4/27 with acute exacerbation of COPD. Ambulated 100 m with PT yesterday without desaturation.

---

## Answer key (generated draft)

**Barriers**

- B-F03 (single-field) — evidence: tracked_fields.caregiver_status, free_text_notes.case_manager_note
- B-C01 (single-field) — evidence: tracked_fields.medication_reconciliation_status
- B-E06 (single-field) — evidence: tracked_fields.medical_device_education_status
- B-C03 (single-field) — evidence: tracked_fields.pending_imaging

**Information gaps**

- none

**Tasks**

- T-CM02 resolves B-F03
- T-PH01 resolves B-C01 — needs sign-off GR-A02 (modify_medication_list)
- T-RN08 resolves B-E06
- T-MD02 resolves B-C03

**Must not flag (negative controls):** B-E03
