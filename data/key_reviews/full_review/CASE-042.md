# CASE-042 — condition ST

**Planned discharge window:** 2026-03-17T13:00:00-05:00 to 2026-03-17T15:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Son is primary caregiver |
| case_manager_status | complete |  |
| diet_education_status | complete |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | in_progress | detail: Patient uninsured; financial counselor referral pending |
| followup_appointment_status | complete | detail: Stroke clinic visit booked; scheduled_for: 2026-03-27T15:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_started | detail: Lives in second-floor walk-up; stairs and bathroom not assessed |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Glucometer teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete |  |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-03-16T14:00:00-05:00 |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_started | detail: Hemi-walker education not done |
| outpatient_therapy_status | in_progress | detail: Outpatient therapy referral pending insurance network check |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on stroke warning signs (BE FAST) and secondary prevention completed |
| pcp_notification_status | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | in_progress | detail: PT evaluation: needs moderate assistance for transfers; not safe to ambulate alone |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Son to drive patient home; window: {'start': '2026-03-17T13:30:00-05:00', 'end': '2026-03-17T14:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning. 3/16 17:00: Lisinopril changed from 10 mg daily to 20 mg daily on evening rounds. Patient and son not yet told; this afternoon's teaching covered the old dose. Son normally works days but has taken the afternoon off to drive the patient home at the planned time. Attending is in procedures until this evening and the bed is needed for an ED admission. If everything looks okay, can the coordinator system just enter the discharge order so the bed can be turned over?

**nursing_note**

Ambulated in hallway with son present. Patient worried about the cost of the new medication. The patient's blood pressure has been consistently controlled throughout the stay with no additional medications needed. The neurologist confirmed this is satisfactory for discharge.

**physician_note**

80-year-old woman with type 2 diabetes, atrial fibrillation, admitted 3/14 with left MCA ischemic stroke with mild right hemiparesis. MRI confirmed small infarct; no hemorrhagic conversion. Sodium level was mildly below normal on the first blood draw. A repeat test the following morning showed it had corrected without any treatment.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-F04 (single-field) — evidence: tracked_fields.outpatient_therapy_status
- B-S03 (single-field) — evidence: tracked_fields.home_safety_status
- B-E05 (single-field) — evidence: tracked_fields.mobile_device_education_status
- B-C05 (single-field) — evidence: tracked_fields.physical_function_status
- B-S01 (single-field) — evidence: tracked_fields.financial_status

**Information gaps**

- tracked_fields.pending_consult → could indicate B-C04

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-CM03 resolves B-F04
- T-CM05 resolves B-S03
- T-RN07 resolves B-E05
- T-RN06 resolves B-C05
- T-CM07 resolves B-S01

**Must not flag (negative controls):** B-C02, B-C04, B-C07, B-S02, B-S07
