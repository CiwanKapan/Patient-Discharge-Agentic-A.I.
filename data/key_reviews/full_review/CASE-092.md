# CASE-092 — condition OR

**Planned discharge window:** 2026-03-30T15:00:00-05:00 to 2026-03-30T17:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Husband will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Orthopedic surgery clinic visit booked; scheduled_for: 2026-04-09T17:00:00-05:00 |
| home_health_referral_status | complete |  |
| home_safety_status | complete |  |
| insurance_authorization_status | complete | detail: DME authorized by insurer |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to CVS |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | complete |  |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on hip/knee precautions and DVT warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Husband to take patient home; window: {'start': '2026-03-30T15:30:00-05:00', 'end': '2026-03-30T16:30:00-05:00'} |
| wound_status | in_progress | detail: Surgical site pain 7/10 despite oral regimen; not yet controlled |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and husband to review the discharge plan.

**nursing_note**

Slept well overnight. Voiding without difficulty.

**physician_note**

81-year-old woman with hypertension, obesity, admitted 3/26 for elective right total knee arthroplasty. Post-op day 3; working with PT twice daily.

---

## Answer key (generated draft)

**Barriers**

- B-C06 (single-field) — evidence: tracked_fields.wound_status

**Information gaps**

- none

**Tasks**

- T-RN05 resolves B-C06

**Must not flag (negative controls):** none
