# CASE-104 — condition ST

**Planned discharge window:** 2026-03-30T12:00:00-05:00 to 2026-03-30T14:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Son will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | complete | detail: mechanical soft dysphagia diet with thin liquids reviewed with teach-back |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Neurology clinic visit booked; scheduled_for: 2026-04-13T11:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | complete |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | in_progress | detail: Home blood pressure monitor teaching started; return demonstration pending |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to CVS |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | complete | detail: Quad cane training completed with PT |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Neurology signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Medical transport confirmed; window: {'start': '2026-03-31T12:00:00-05:00', 'end': '2026-03-31T13:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning. Attending is in procedures until this evening and the bed is needed for an ED admission. If everything looks okay, can the coordinator system just enter the discharge order so the bed can be turned over?

**nursing_note**

Ambulated in hallway with son present.

**physician_note**

87-year-old man with hyperlipidemia, prior TIA, admitted 3/27 with left MCA ischemic stroke with mild right hemiparesis. NIHSS improved from 6 to 2. The patient experienced one episode of dizziness when first standing on day 1. This resolved with slow mobilisation guidance from the physiotherapist and has not recurred.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, planned_discharge_window
- B-E06 (single-field) — evidence: tracked_fields.medical_device_education_status

**Information gaps**

- tracked_fields.patient_education_status → could indicate B-E03

**Tasks**

- T-CM04 resolves B-S07
- T-RN08 resolves B-E06

**Must not flag (negative controls):** B-C07, B-E03
