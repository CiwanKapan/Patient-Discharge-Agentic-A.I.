# CASE-154 — condition OR

**Planned discharge window:** 2026-03-23T09:00:00-05:00 to 2026-03-23T11:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Nephew will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Orthopedic surgery clinic visit booked; scheduled_for: 2026-04-04T11:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | complete | detail: Single-level home; grab bars installed |
| insurance_authorization_status | in_progress | detail: Prior authorization for knee scooter and home PT submitted; decision pending |
| medical_device_education_status | complete | detail: Incision vacuum dressing teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to Walgreens |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | complete | detail: Knee scooter training completed with PT |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on hip/knee precautions and DVT warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Internal medicine (co-management) signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Nephew to drive patient home; documented_at: 2026-03-22T09:00:00-05:00; window: {'start': '2026-03-23T09:00:00-05:00', 'end': '2026-03-23T10:00:00-05:00'} |
| wound_status | in_progress | detail: Surgical site pain 7/10 despite oral regimen; not yet controlled |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning. 3/23 07:00: Nephew tested positive for COVID and cannot pick the patient up. Patient does not drive; no other ride identified.

**nursing_note**

Vitals stable this shift. Tolerating diet. The patient is on a controlled medication that requires a special prescription. This was prepared and reviewed by the pharmacist before discharge, and everything is in order.

**physician_note**

70-year-old woman with hypothyroidism, osteoarthritis, admitted 3/19 for elective right total knee arthroplasty. Post-op day 3; working with PT twice daily.

---

## Answer key (generated draft)

**Barriers**

- B-S02 (single-field) — evidence: tracked_fields.transport_status, free_text_notes.case_manager_note
- B-S04 (single-field) — evidence: tracked_fields.insurance_authorization_status
- B-C06 (single-field) — evidence: tracked_fields.wound_status

**Information gaps**

- none

**Tasks**

- T-CM04 resolves B-S02
- T-CM06 resolves B-S04
- T-RN05 resolves B-C06

**Must not flag (negative controls):** B-C01, B-E02
