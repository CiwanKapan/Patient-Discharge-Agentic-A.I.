# CASE-030 — condition HF

**Planned discharge window:** 2026-06-22T14:00:00-05:00 to 2026-06-22T16:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Sister will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | complete | detail: 2 g sodium and 2 L fluid restriction reviewed with teach-back |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | not_started | detail: Cardiology clinic follow-up not yet booked |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Home scale and blood pressure cuff teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to Walgreens |
| medication_education_status | complete |  |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | not_started | detail: Teaching on daily weights and heart failure symptom monitoring not yet done |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Nephrology signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Sister to drive patient home; documented_at: 2026-06-21T13:00:00-05:00; window: {'start': '2026-06-22T14:00:00-05:00', 'end': '2026-06-22T15:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with sister. 6/22 13:00: Sister tested positive for COVID and cannot pick the patient up. Patient does not drive; no other ride identified. Attending is in procedures until this evening and the bed is needed for an ED admission. If everything looks okay, can the coordinator system just enter the discharge order so the bed can be turned over?

**nursing_note**

Up in chair for meals. Pain controlled. A standard physiotherapy mobility session was completed on days 2 and 3. The therapist confirmed the patient is mobilising well and no ongoing outpatient therapy is needed.

**physician_note**

62-year-old man with CAD s/p PCI, atrial fibrillation, admitted 6/18 with HFpEF exacerbation precipitated by dietary sodium excess. Diuresed 6 kg with IV furosemide; now euvolemic on oral regimen.

---

## Answer key (generated draft)

**Barriers**

- B-S02 (single-field) — evidence: tracked_fields.transport_status, free_text_notes.case_manager_note
- B-E03 (single-field) — evidence: tracked_fields.patient_education_status
- B-F01 (single-field) — evidence: tracked_fields.followup_appointment_status

**Information gaps**

- none

**Tasks**

- T-CM04 resolves B-S02
- T-RN02 resolves B-E03
- T-CM01 resolves B-F01

**Must not flag (negative controls):** B-C05
