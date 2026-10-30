# CASE-002 — condition ST

**Planned discharge window:** 2026-04-15T09:00:00-05:00 to 2026-04-15T11:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Daughter is primary caregiver; works days, available evenings; window: {'start': '2026-04-15T18:00:00-05:00', 'end': '2026-04-15T22:00:00-05:00'} |
| case_manager_status | complete |  |
| diet_education_status | complete | detail: mechanical soft dysphagia diet with thin liquids reviewed with teach-back |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Stroke clinic visit booked; scheduled_for: 2026-04-27T10:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | complete |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to CVS |
| medication_education_status | in_progress | detail: Teaching on clopidogrel 75 mg daily x21 days with aspirin started; teach-back not completed |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | complete | detail: Wheelchair training completed with PT |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on stroke warning signs (BE FAST) and secondary prevention completed |
| pcp_notification_status | complete |  |
| pending_consult | unknown | detail: Not documented |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Daughter to drive patient home after work; window: {'start': '2026-04-15T18:30:00-05:00', 'end': '2026-04-15T19:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning.

**nursing_note**

Ambulated in hallway with daughter present. A blood sugar reading was briefly elevated on the morning of day 2. The patient's insulin was adjusted slightly and all subsequent readings have been within the target range.

**physician_note**

63-year-old man with hyperlipidemia, hypertension, admitted 4/8 with small right cerebellar infarct. NIHSS improved from 6 to 2.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, tracked_fields.caregiver_status, planned_discharge_window
- B-E01 (single-field) — evidence: tracked_fields.medication_education_status

**Information gaps**

- tracked_fields.pending_consult → could indicate B-C04

**Tasks**

- T-CM04 resolves B-S07
- T-RN01 resolves B-E01

**Must not flag (negative controls):** B-C02, B-C04
