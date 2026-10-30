# CASE-015 — condition OR

**Planned discharge window:** 2026-06-08T14:00:00-05:00 to 2026-06-08T16:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Wife will stay with patient for the first week |
| case_manager_status | in_progress | detail: Assigned case manager out sick; coverage not confirmed |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete |  |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Orthopedic surgery clinic visit booked (first available); scheduled_for: 2026-07-15T09:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_started | detail: Lives in second-floor walk-up; stairs and bathroom not assessed |
| insurance_authorization_status | complete | detail: DME authorized by insurer |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to a local independent pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | complete |  |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on hip/knee precautions and DVT warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | unknown | detail: No documentation found in chart |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Wife to take patient home; window: {'start': '2026-06-08T14:30:00-05:00', 'end': '2026-06-08T15:30:00-05:00'} |
| wound_status | in_progress | detail: Surgical site pain 7/10 despite oral regimen; not yet controlled |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning.

**nursing_note**

Up in chair for meals. Pain controlled.

**physician_note**

57-year-old man with obesity, hypertension, admitted 6/1 for elective right total knee arthroplasty. Post-op day 6; tolerating diet, voiding. Needs orthopedic surgery clinic follow-up within 14 days of discharge. The patient reported mild nausea on the morning of day 2. This was managed with a standard anti-nausea medication and the patient has been eating and drinking normally since.

---

## Answer key (generated draft)

**Barriers**

- B-S05 (single-field) — evidence: tracked_fields.case_manager_status
- B-S03 (single-field) — evidence: tracked_fields.home_safety_status
- B-C06 (single-field) — evidence: tracked_fields.wound_status

**Information gaps**

- tracked_fields.pending_consult → could indicate B-C04

**Tasks**

- T-CM09 resolves B-S05
- T-CM05 resolves B-S03
- T-RN05 resolves B-C06

**Must not flag (negative controls):** B-C04
