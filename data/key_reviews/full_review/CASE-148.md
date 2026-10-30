# CASE-148 — condition OR

**Planned discharge window:** 2026-03-26T12:00:00-05:00 to 2026-03-26T14:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Nephew will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Orthopedic surgery clinic visit booked; scheduled_for: 2026-04-02T12:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | complete | detail: Single-level home; grab bars installed |
| insurance_authorization_status | complete | detail: DME authorized by insurer |
| medical_device_education_status | complete | detail: Cold therapy unit teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete |  |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | complete | detail: Knee scooter training completed with PT |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Internal medicine (co-management) signed off |
| pending_imaging | complete |  |
| pending_labs | complete |  |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Nephew will pick patient up; window: {'start': '2026-03-26T17:00:00-05:00', 'end': '2026-03-26T18:00:00-05:00'} |
| wound_status | in_progress | detail: Surgical site pain 7/10 despite oral regimen; not yet controlled |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with nephew.

**nursing_note**

Slept well overnight. Voiding without difficulty. The patient's regular heartburn medication was changed to a different brand during the stay due to supply. The patient was told about this, and both brands are the same medication at the same dose.

**physician_note**

74-year-old man with obesity, hypothyroidism, admitted 3/22 for ORIF of right bimalleolar ankle fracture. Post-op day 3; working with PT twice daily.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, planned_discharge_window
- B-C06 (single-field) — evidence: tracked_fields.wound_status

**Information gaps**

- none

**Tasks**

- T-CM04 resolves B-S07
- T-RN05 resolves B-C06

**Must not flag (negative controls):** B-C01, B-E01
