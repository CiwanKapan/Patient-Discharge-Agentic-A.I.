# CASE-020 — condition OR

**Planned discharge window:** 2026-05-18T09:00:00-05:00 to 2026-05-18T11:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Daughter will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Orthopedic surgery clinic visit booked; scheduled_for: 2026-05-31T09:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | unknown | detail: No documentation found in chart |
| insurance_authorization_status | in_progress | detail: Prior authorization for rolling walker and home PT submitted; decision pending |
| medical_device_education_status | complete | detail: Continuous passive motion machine teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete |  |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-05-17T14:00:00-05:00 |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | complete | detail: Rolling walker training completed with PT |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on hip/knee precautions and DVT warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Wound care signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | not_started | detail: No ride home arranged; patient does not drive |
| wound_status | complete |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning. 5/17 17:00: Metoprolol tartrate changed from 25 mg twice daily to 12.5 mg twice daily on evening rounds. Patient and daughter not yet told; this afternoon's teaching covered the old dose. Patient asked how they are getting home; no ride yet.

**nursing_note**

Ambulated in hallway with daughter present. The patient has a close friend who visits weekly and helps with shopping. This was noted as a positive social support factor. No concerns were raised about the patient's social situation.

**physician_note**

88-year-old man with obesity, hypertension, admitted 5/11 for left total hip arthroplasty. Post-op day 6; tolerating diet, voiding.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-S02 (single-field) — evidence: tracked_fields.transport_status
- B-S04 (single-field) — evidence: tracked_fields.insurance_authorization_status

**Information gaps**

- tracked_fields.home_safety_status → could indicate B-S03

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-CM04 resolves B-S02
- T-CM06 resolves B-S04

**Must not flag (negative controls):** B-F03, B-S03
