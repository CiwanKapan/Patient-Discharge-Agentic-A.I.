# CASE-147 — condition ST

**Planned discharge window:** 2026-04-16T10:00:00-05:00 to 2026-04-16T12:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Husband will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | complete | detail: mechanical soft dysphagia diet with thin liquids reviewed with teach-back |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Neurology clinic visit booked; scheduled_for: 2026-04-29T09:00:00-05:00 |
| home_health_referral_status | complete |  |
| home_safety_status | in_progress | detail: OT flagged tub shower and no grab bars; modifications not arranged |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to Walgreens |
| medication_education_status | complete |  |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_started | detail: Hemi-walker education not done |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Wheelchair van to take patient home; window: {'start': '2026-04-16T10:30:00-05:00', 'end': '2026-04-16T11:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning.

**nursing_note**

Ambulated in hallway with husband present.

**physician_note**

86-year-old woman with type 2 diabetes, prior TIA, admitted 4/9 with right pontine lacunar infarct. NIHSS improved from 6 to 2.

---

## Answer key (generated draft)

**Barriers**

- B-E05 (single-field) — evidence: tracked_fields.mobile_device_education_status
- B-S03 (single-field) — evidence: tracked_fields.home_safety_status

**Information gaps**

- none

**Tasks**

- T-RN07 resolves B-E05
- T-CM05 resolves B-S03

**Must not flag (negative controls):** none
