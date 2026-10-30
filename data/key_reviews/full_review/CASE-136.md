# CASE-136 — condition HF

**Planned discharge window:** 2026-04-23T09:00:00-05:00 to 2026-04-23T11:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Nephew is primary caregiver |
| case_manager_status | complete |  |
| diet_education_status | not_started | detail: 2 g sodium and 2 L fluid restriction not yet reviewed with patient |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Cardiology clinic visit booked; scheduled_for: 2026-04-27T09:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Telemonitoring scale teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete |  |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-04-22T14:00:00-05:00 |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on daily weights and heart failure symptom monitoring completed |
| pcp_notification_status | complete |  |
| pending_consult | in_progress | detail: Electrophysiology consult requested yesterday; recommendations not yet documented |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Nephew to drive patient home; window: {'start': '2026-04-23T09:30:00-05:00', 'end': '2026-04-23T10:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning. 4/22 18:00: Per pharmacy, metoprolol succinate changed from 25 mg daily to 50 mg daily. No documentation that the patient or family has been informed of the new dose. Nephew normally works days but has taken the afternoon off to drive the patient home at the planned time.

**nursing_note**

Up in chair for meals. Pain controlled. The patient's spouse was present for most of the stay and is well-informed about the care plan. They expressed no concerns and are ready to support the patient at home.

**physician_note**

53-year-old woman with type 2 diabetes, atrial fibrillation, admitted 4/18 with HFpEF exacerbation precipitated by dietary sodium excess. Net negative 6.4 L this admission; dyspnea back to baseline.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-E04 (single-field) — evidence: tracked_fields.diet_education_status
- B-C04 (single-field) — evidence: tracked_fields.pending_consult

**Information gaps**

- none

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-RN03 resolves B-E04
- T-MD03 resolves B-C04

**Must not flag (negative controls):** B-F03, B-S02, B-S07
