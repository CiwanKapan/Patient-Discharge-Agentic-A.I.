# CASE-128 — condition ST

**Planned discharge window:** 2026-03-19T08:00:00-05:00 to 2026-03-19T10:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Wife will stay with patient for the first week |
| case_manager_status | in_progress | detail: Assigned case manager out sick; coverage not confirmed |
| diet_education_status | complete | detail: mechanical soft dysphagia diet with thin liquids reviewed with teach-back |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Stroke clinic visit booked; scheduled_for: 2026-03-26T09:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | complete |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to the hospital outpatient pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-03-18T14:00:00-05:00 |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | in_progress | detail: Quad cane training started; patient not yet safe on stairs |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | not_started | detail: PCP not yet notified of admission or medication changes |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Wife to take patient home; window: {'start': '2026-03-19T08:30:00-05:00', 'end': '2026-03-19T09:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and wife to review the discharge plan. 3/18 19:00: Atorvastatin changed from 20 mg daily to 80 mg daily on evening rounds. Patient and wife not yet told; this afternoon's teaching covered the old dose.

**nursing_note**

Ambulated in hallway with wife present. Need to update the PCP before discharge. A mild rash appeared briefly at the IV insertion site on day 2. It was assessed as a minor irritation, treated with a topical cream, and has fully resolved.

**physician_note**

52-year-old man with prior TIA, atrial fibrillation, admitted 3/15 with small right cerebellar infarct. Deficits stable for 48 hours; passed bedside swallow.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-S05 (single-field) — evidence: tracked_fields.case_manager_status
- B-F05 (single-field) — evidence: tracked_fields.pcp_notification_status
- B-E05 (single-field) — evidence: tracked_fields.mobile_device_education_status

**Information gaps**

- none

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-CM09 resolves B-S05
- T-CM08 resolves B-F05
- T-RN07 resolves B-E05

**Must not flag (negative controls):** none
