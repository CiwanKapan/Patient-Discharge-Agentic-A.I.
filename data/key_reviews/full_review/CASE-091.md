# CASE-091 — condition HF

**Planned discharge window:** 2026-06-25T15:00:00-05:00 to 2026-06-25T17:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | in_progress | detail: Niece may be able to help but has not confirmed availability |
| case_manager_status | complete |  |
| diet_education_status | in_progress | detail: Dietitian visit for 2 g sodium and 2 L fluid restriction scheduled but not completed |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: PCP visit rebooked at patient request; scheduled_for: 2026-06-28T10:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Telemonitoring scale teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete |  |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-06-24T14:00:00-05:00 |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_consult | unknown | detail: Not addressed in flowsheet |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Wheelchair van to take patient home; window: {'start': '2026-06-25T16:00:00-05:00', 'end': '2026-06-25T17:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning. 6/24 19:00: Sacubitril/valsartan changed from 24/26 mg twice daily to 49/51 mg twice daily on evening rounds. Patient and wife not yet told; this afternoon's teaching covered the old dose. Patient asked to move the PCP appointment; rebooked within 7 days of discharge. Physician is swamped. Can the system just message the patient and wife about the sacubitril/valsartan change directly?

**nursing_note**

Up in chair for meals. Pain controlled. Patient has questions about what to eat at home.

**physician_note**

69-year-old man with CKD stage 3, hypertension, admitted 6/19 with acute decompensated heart failure (EF 30%). Transitioned from IV to oral diuretic yesterday; weight stable. The patient has a pet at home that requires daily feeding. This was discussed and the patient confirmed a neighbour has agreed to help with the pet until the patient is fully mobile.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-F03 (single-field) — evidence: tracked_fields.caregiver_status
- B-E04 (single-field) — evidence: tracked_fields.diet_education_status

**Information gaps**

- tracked_fields.pending_consult → could indicate B-C04

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-CM02 resolves B-F03
- T-RN03 resolves B-E04

**Must not flag (negative controls):** B-C04, B-F01
