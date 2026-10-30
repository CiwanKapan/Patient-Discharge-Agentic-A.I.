# CASE-112 — condition HF

**Planned discharge window:** 2026-03-16T11:00:00-05:00 to 2026-03-16T13:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete |  |
| case_manager_status | complete |  |
| diet_education_status | in_progress | detail: Dietitian visit for 2 g sodium and 2 L fluid restriction scheduled but not completed |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Heart failure clinic visit booked; scheduled_for: 2026-03-22T12:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Home scale and blood pressure cuff teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete |  |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-03-15T14:00:00-05:00 |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on daily weights and heart failure symptom monitoring completed |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | in_progress | detail: Repeat BNP resulted overnight but not yet reviewed by physician |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Sister to take patient home; window: {'start': '2026-03-16T11:00:00-05:00', 'end': '2026-03-16T12:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with sister. 3/15 19:00: Per pharmacy, sacubitril/valsartan changed from 24/26 mg twice daily to 49/51 mg twice daily. No documentation that the patient or family has been informed of the new dose.

**nursing_note**

Slept well overnight. Voiding without difficulty.

**physician_note**

70-year-old man with CKD stage 3, atrial fibrillation, admitted 3/9 with new-onset heart failure with reduced ejection fraction. Net negative 5.1 L this admission; dyspnea back to baseline. The patient reported mild back pain on day 2. This was assessed as positional discomfort from bed rest. Pain resolved with repositioning and a mild pain reliever. No further concern.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-E04 (single-field) — evidence: tracked_fields.diet_education_status
- B-C02 (single-field) — evidence: tracked_fields.pending_labs

**Information gaps**

- none

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-RN03 resolves B-E04
- T-MD02 resolves B-C02

**Must not flag (negative controls):** none
