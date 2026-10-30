# CASE-047 — condition OR

**Planned discharge window:** 2026-05-19T14:00:00-05:00 to 2026-05-19T16:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Son will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Orthopedic surgery clinic visit booked; scheduled_for: 2026-05-22T15:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | in_progress | detail: OT flagged tub shower and no grab bars; modifications not arranged |
| insurance_authorization_status | unknown | detail: Not documented |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to a local independent pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-05-18T14:00:00-05:00 |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | complete | detail: Knee scooter training completed with PT |
| outpatient_therapy_status | in_progress | detail: Outpatient therapy referral pending insurance network check |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on hip/knee precautions and DVT warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete |  |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Son to take patient home; window: {'start': '2026-05-19T15:00:00-05:00', 'end': '2026-05-19T16:00:00-05:00'} |
| wound_status | in_progress | detail: Incision with new serous drainage and surrounding erythema; wound team to reassess |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with son. 5/18 19:00: Per pharmacy, aspirin changed from 81 mg daily to 81 mg twice daily for DVT prophylaxis. No documentation that the patient or family has been informed of the new dose.

**nursing_note**

Ambulated in hallway with son present. Bedroom is upstairs at home; setup not reviewed yet.

**physician_note**

63-year-old woman with obesity, hypothyroidism, admitted 5/16 for left total hip arthroplasty. Post-op day 2; working with PT twice daily. A standard social work screening was completed on admission. The patient did not meet the criteria for a social work referral and no further input was needed.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-C06 (single-field) — evidence: tracked_fields.wound_status
- B-S03 (single-field) — evidence: tracked_fields.home_safety_status
- B-F04 (single-field) — evidence: tracked_fields.outpatient_therapy_status

**Information gaps**

- tracked_fields.insurance_authorization_status → could indicate B-S04

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-RN05 resolves B-C06
- T-CM05 resolves B-S03
- T-CM03 resolves B-F04

**Must not flag (negative controls):** B-F03, B-S01, B-S04
