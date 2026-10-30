# CASE-004 — condition OR

**Planned discharge window:** 2026-04-24T10:00:00-05:00 to 2026-04-24T12:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Sister will stay with patient for the first week |
| case_manager_status | in_progress | detail: Assigned case manager out sick; coverage not confirmed |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Orthopedic surgery clinic visit booked; scheduled_for: 2026-04-29T10:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | complete | detail: Single-level home; grab bars installed |
| insurance_authorization_status | complete | detail: DME authorized by insurer |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete |  |
| medication_availability_status | complete | detail: Discharge prescriptions sent to the hospital outpatient pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-04-23T14:00:00-05:00 |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | complete |  |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on hip/knee precautions and DVT warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Physical medicine and rehabilitation signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Wheelchair van to take patient home; window: {'start': '2026-04-24T11:00:00-05:00', 'end': '2026-04-24T12:00:00-05:00'} |
| wound_status | complete | detail: Incision clean, dry and intact |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning. 4/23 17:00: Per pharmacy, aspirin changed from 81 mg daily to 81 mg twice daily for DVT prophylaxis. No documentation that the patient or family has been informed of the new dose.

**nursing_note**

Slept well overnight. Voiding without difficulty. Blood pressure was elevated on arrival. It has been consistently within the normal range for the past 48 hours.

**physician_note**

65-year-old woman with hypertension, osteoarthritis, admitted 4/20 for left total hip arthroplasty. Post-op day 3; pain controlled on oral regimen.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-S05 (single-field) — evidence: tracked_fields.case_manager_status

**Information gaps**

- none

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-CM09 resolves B-S05

**Must not flag (negative controls):** B-C07
