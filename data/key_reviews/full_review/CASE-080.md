# CASE-080 — condition ST

**Planned discharge window:** 2026-03-12T10:00:00-05:00 to 2026-03-12T12:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Nephew is primary caregiver; works days, available evenings; window: {'start': '2026-03-12T18:00:00-05:00', 'end': '2026-03-12T22:00:00-05:00'} |
| case_manager_status | complete |  |
| diet_education_status | complete | detail: mechanical soft dysphagia diet with thin liquids reviewed with teach-back |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Stroke clinic visit booked; scheduled_for: 2026-03-23T15:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | complete | detail: Single-level home; grab bars installed |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Glucometer teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete |  |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list, including the dose change; documented_at: 2026-03-11T15:00:00-05:00 |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_started | detail: Hemi-walker education not done |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | unknown | detail: Not documented |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Neurology signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Nephew to drive patient home after work; window: {'start': '2026-03-12T18:30:00-05:00', 'end': '2026-03-12T19:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning.

**nursing_note**

Up in chair for meals. Pain controlled. 3/11 15:00: Lisinopril changed from 10 mg daily to 20 mg daily this morning. Reviewed with patient and nephew at 15:00; teach-back correct. A routine palliative care screening question was included in the admission assessment as per standard protocol. The patient did not meet the criteria for a palliative care referral.

**physician_note**

58-year-old woman with prior TIA, hypertension, admitted 3/9 with left thalamic infarct with sensory deficits. MRI confirmed small infarct; no hemorrhagic conversion.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, tracked_fields.caregiver_status, planned_discharge_window
- B-E05 (single-field) — evidence: tracked_fields.mobile_device_education_status

**Information gaps**

- tracked_fields.patient_education_status → could indicate B-E03

**Tasks**

- T-CM04 resolves B-S07
- T-RN07 resolves B-E05

**Must not flag (negative controls):** B-E01, B-E03, B-E07
