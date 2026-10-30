# CASE-060 — condition ST

**Planned discharge window:** 2026-03-24T11:00:00-05:00 to 2026-03-24T13:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Son is primary caregiver |
| case_manager_status | complete |  |
| diet_education_status | not_started | detail: Mechanical soft dysphagia diet with thin liquids not yet reviewed with patient |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Neurology clinic visit booked; scheduled_for: 2026-04-05T10:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_started | detail: Lives in second-floor walk-up; stairs and bathroom not assessed |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Home blood pressure monitor teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds; documented_at: 2026-03-23T10:00:00-05:00 |
| medication_availability_status | complete | detail: Discharge prescriptions sent to the hospital outpatient pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | not_started | detail: Quad cane education not done |
| outpatient_therapy_status | complete |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on stroke warning signs (BE FAST) and secondary prevention completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Speech-language pathology signed off |
| pending_imaging | complete |  |
| pending_labs | complete |  |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Son to drive patient home; window: {'start': '2026-03-24T11:30:00-05:00', 'end': '2026-03-24T12:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and son to review the discharge plan. Patient has questions about what to eat at home. Son normally works days but has taken the afternoon off to drive the patient home at the planned time.

**nursing_note**

Slept well overnight. Voiding without difficulty. Bedroom is upstairs at home; setup not reviewed yet.

**physician_note**

54-year-old man with atrial fibrillation, prior TIA, admitted 3/21 with left MCA ischemic stroke with mild right hemiparesis. MRI confirmed small infarct; no hemorrhagic conversion. 3/24 10:00: New right arm drift at 13:00 (NIHSS up from 2 to 5); repeat imaging ordered. The patient was treated for shingles approximately two years ago. The condition fully resolved and no residual effects were noted during this admission.

---

## Answer key (generated draft)

**Barriers**

- B-C07 (single-field) — evidence: tracked_fields.medical_stability_status, free_text_notes.physician_note
- B-S03 (single-field) — evidence: tracked_fields.home_safety_status
- B-E05 (single-field) — evidence: tracked_fields.mobile_device_education_status
- B-E04 (single-field) — evidence: tracked_fields.diet_education_status

**Information gaps**

- none

**Tasks**

- T-MD04 resolves B-C07 — needs sign-off GR-A07 (escalate_to_attending_physician)
- T-CM05 resolves B-S03
- T-RN07 resolves B-E05
- T-RN03 resolves B-E04

**Must not flag (negative controls):** B-S02, B-S07
