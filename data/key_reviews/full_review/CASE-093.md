# CASE-093 — condition ST

**Planned discharge window:** 2026-06-15T15:00:00-05:00 to 2026-06-15T17:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Sister will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | complete |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Stroke clinic visit booked; scheduled_for: 2026-06-23T14:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | complete | detail: Single-level home; grab bars installed |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to Walgreens |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-06-14T14:00:00-05:00 |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | complete | detail: Quad cane training completed with PT |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on stroke warning signs (BE FAST) and secondary prevention completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Neurology signed off |
| pending_imaging | in_progress | detail: Carotid ultrasound completed; awaiting radiology read |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Sister to take patient home; window: {'start': '2026-06-15T15:30:00-05:00', 'end': '2026-06-15T16:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and sister to review the discharge plan. 6/14 19:00: Per pharmacy, lisinopril changed from 10 mg daily to 20 mg daily. No documentation that the patient or family has been informed of the new dose. Radiology read on the carotid ultrasound still pending.

**nursing_note**

Slept well overnight. Voiding without difficulty.

**physician_note**

74-year-old woman with prior TIA, hyperlipidemia, admitted 6/8 with right pontine lacunar infarct. NIHSS improved from 6 to 2. The patient receives home care visits twice a week for personal care. This existing service was confirmed as still in place and the home-care provider has been notified of the discharge date.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-C03 (single-field) — evidence: tracked_fields.pending_imaging

**Information gaps**

- none

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-MD02 resolves B-C03

**Must not flag (negative controls):** B-F03
