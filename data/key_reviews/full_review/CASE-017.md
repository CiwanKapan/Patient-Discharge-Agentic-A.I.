# CASE-017 — condition ST

**Planned discharge window:** 2026-03-09T12:00:00-05:00 to 2026-03-09T14:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Husband is primary caregiver; works days, available evenings; window: {'start': '2026-03-09T17:00:00-05:00', 'end': '2026-03-09T21:00:00-05:00'} |
| case_manager_status | complete |  |
| diet_education_status | complete | detail: mechanical soft dysphagia diet with thin liquids reviewed with teach-back |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Neurology clinic visit booked; scheduled_for: 2026-03-17T11:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | complete | detail: Single-level home; grab bars installed |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete |  |
| medication_availability_status | complete | detail: Discharge prescriptions sent to CVS |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | complete | detail: Hemi-walker training completed with PT |
| outpatient_therapy_status | not_started | detail: Outpatient PT/OT referral not placed |
| oxygen_requirement | not_applicable |  |
| patient_education_status | unknown | detail: Not addressed in flowsheet |
| pcp_notification_status | complete |  |
| pending_consult | in_progress | detail: Neurology consult requested yesterday; recommendations not yet documented |
| pending_imaging | in_progress | detail: Carotid ultrasound completed; awaiting radiology read |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Husband to drive patient home after work; window: {'start': '2026-03-09T17:30:00-05:00', 'end': '2026-03-09T18:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and husband to review the discharge plan.

**nursing_note**

Ambulated in hallway with husband present. Therapy referral still needs to be sent. Radiology read on the carotid ultrasound still pending. Neurology has not seen the patient yet.

**physician_note**

83-year-old woman with hypertension, atrial fibrillation, admitted 3/2 with small right cerebellar infarct. MRI confirmed small infarct; no hemorrhagic conversion. The patient requested information about a herbal supplement they take at home. The pharmacist reviewed it and confirmed it is safe to continue with no interactions.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, tracked_fields.caregiver_status, planned_discharge_window
- B-F04 (single-field) — evidence: tracked_fields.outpatient_therapy_status
- B-C03 (single-field) — evidence: tracked_fields.pending_imaging
- B-C04 (single-field) — evidence: tracked_fields.pending_consult

**Information gaps**

- tracked_fields.patient_education_status → could indicate B-E03

**Tasks**

- T-CM04 resolves B-S07
- T-CM03 resolves B-F04
- T-MD02 resolves B-C03
- T-MD03 resolves B-C04

**Must not flag (negative controls):** B-C01, B-E03
