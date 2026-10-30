# CASE-158 — condition ST

**Planned discharge window:** 2026-05-25T14:00:00-05:00 to 2026-05-25T16:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | not_started | detail: No caregiver identified; patient lives alone and needs help with ADLs |
| case_manager_status | complete |  |
| diet_education_status | complete | detail: mechanical soft dysphagia diet with thin liquids reviewed with teach-back |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Stroke clinic visit booked; scheduled_for: 2026-05-31T13:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | complete |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete |  |
| medication_availability_status | complete | detail: Discharge prescriptions sent to CVS; documented_at: 2026-05-24T11:00:00-05:00 |
| medication_education_status | complete |  |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | in_progress | detail: Wheelchair training started; patient not yet safe on stairs |
| outpatient_therapy_status | not_started | detail: Outpatient PT/OT referral not placed |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on stroke warning signs (BE FAST) and secondary prevention completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Cardiology (for loop recorder) signed off |
| pending_imaging | complete |  |
| pending_labs | unknown | detail: Not addressed in flowsheet |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Sister will pick patient up before work; window: {'start': '2026-05-25T07:00:00-05:00', 'end': '2026-05-25T08:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning.

**nursing_note**

Vitals stable this shift. Tolerating diet. 5/25 12:00: CVS called: atorvastatin is out of stock until next week. No alternate pharmacy arranged.

**physician_note**

75-year-old man with atrial fibrillation, hypertension, admitted 5/20 with left thalamic infarct with sensory deficits. Deficits stable for 48 hours; passed bedside swallow. The patient has a well-healed surgical scar on the abdomen from an operation several years ago. No wound care is needed and this has no impact on the discharge plan. A routine review of the patient's long-term conditions was completed by the attending physician. No new diagnoses were made and no changes to ongoing management were recommended.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, planned_discharge_window
- B-E02 (single-field) — evidence: tracked_fields.medication_availability_status, free_text_notes.nursing_note
- B-F03 (single-field) — evidence: tracked_fields.caregiver_status
- B-E05 (single-field) — evidence: tracked_fields.mobile_device_education_status
- B-F04 (single-field) — evidence: tracked_fields.outpatient_therapy_status

**Information gaps**

- tracked_fields.pending_labs → could indicate B-C02

**Tasks**

- T-CM04 resolves B-S07
- T-PH02 resolves B-E02 — needs sign-off GR-A03 (send_prescription)
- T-CM02 resolves B-F03
- T-RN07 resolves B-E05
- T-CM03 resolves B-F04

**Must not flag (negative controls):** B-C02
