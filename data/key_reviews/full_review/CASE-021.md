# CASE-021 — condition HF

**Planned discharge window:** 2026-06-22T14:00:00-05:00 to 2026-06-22T16:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Son is primary caregiver |
| case_manager_status | complete |  |
| diet_education_status | complete |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Cardiology clinic visit booked; scheduled_for: 2026-06-28T14:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Telemonitoring scale teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds; documented_at: 2026-06-21T11:00:00-05:00 |
| medication_availability_status | complete |  |
| medication_education_status | not_started | detail: No teaching yet on new spironolactone 25 mg daily |
| medication_reconciliation_status | in_progress | detail: Discrepancy between home and inpatient sacubitril/valsartan doses not yet resolved |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete |  |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Son to drive patient home; window: {'start': '2026-06-22T14:30:00-05:00', 'end': '2026-06-22T15:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with son. Patient asked what the new spironolactone 25 mg daily is for; teaching still needed. Earlier pickup was cancelled and rebooked for 14:30 to match the discharge time.

**nursing_note**

Slept well overnight. Voiding without difficulty. The patient's spouse was present for most of the stay and is well-informed about the care plan. They expressed no concerns and are ready to support the patient at home.

**physician_note**

52-year-old woman with hypertension, atrial fibrillation, admitted 6/18 with acute decompensated heart failure (EF 30%). Transitioned from IV to oral diuretic yesterday; weight stable. 6/22 12:20: Creatinine rose from 1.4 to 2.1 after diuresis; holding diuretics and rechecking.

---

## Answer key (generated draft)

**Barriers**

- B-C07 (single-field) — evidence: tracked_fields.medical_stability_status, free_text_notes.physician_note
- B-C01 (single-field) — evidence: tracked_fields.medication_reconciliation_status
- B-E01 (single-field) — evidence: tracked_fields.medication_education_status

**Information gaps**

- none

**Tasks**

- T-MD04 resolves B-C07 — needs sign-off GR-A07 (escalate_to_attending_physician)
- T-PH01 resolves B-C01 — needs sign-off GR-A02 (modify_medication_list)
- T-RN01 resolves B-E01

**Must not flag (negative controls):** B-F03, B-S02, B-S07
