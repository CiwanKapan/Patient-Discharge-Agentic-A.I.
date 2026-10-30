# CASE-037 — condition OR

**Planned discharge window:** 2026-03-09T15:00:00-05:00 to 2026-03-09T17:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Daughter will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Orthopedic surgery clinic visit booked; scheduled_for: 2026-03-16T17:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | complete | detail: Single-level home; grab bars installed |
| insurance_authorization_status | in_progress | detail: Insurance authorization for short-term rehab placement pending |
| medical_device_education_status | complete |  |
| medical_stability_status | complete |  |
| medication_availability_status | complete | detail: Discharge prescriptions sent to CVS |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | complete | detail: Knee scooter training completed with PT |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Wound care signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Medical transport to take patient home; window: {'start': '2026-03-09T16:00:00-05:00', 'end': '2026-03-09T17:00:00-05:00'} |
| wound_status | in_progress | detail: Incision with new serous drainage and surrounding erythema; wound team to reassess |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning.

**nursing_note**

Ambulated in hallway with daughter present.

**physician_note**

54-year-old woman with hypothyroidism, type 2 diabetes, admitted 3/6 for elective right total knee arthroplasty. Post-op day 2; working with PT twice daily.

---

## Answer key (generated draft)

**Barriers**

- B-C06 (single-field) — evidence: tracked_fields.wound_status
- B-S04 (single-field) — evidence: tracked_fields.insurance_authorization_status

**Information gaps**

- none

**Tasks**

- T-RN05 resolves B-C06
- T-CM06 resolves B-S04

**Must not flag (negative controls):** none
