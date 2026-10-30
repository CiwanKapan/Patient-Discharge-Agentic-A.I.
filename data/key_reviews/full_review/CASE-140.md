# CASE-140 — condition OR

**Planned discharge window:** 2026-03-16T14:00:00-05:00 to 2026-03-16T16:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Sister is primary caregiver; works days, available evenings; window: {'start': '2026-03-16T17:00:00-05:00', 'end': '2026-03-16T21:00:00-05:00'} |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Orthopedic surgery clinic visit booked; scheduled_for: 2026-03-27T15:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | complete | detail: Single-level home; grab bars installed |
| insurance_authorization_status | complete |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete |  |
| medication_availability_status | complete | detail: Discharge prescriptions sent to a local independent pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | complete | detail: Knee scooter training completed with PT |
| outpatient_therapy_status | not_started | detail: Outpatient PT/OT referral not placed |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on hip/knee precautions and DVT warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | unknown | detail: Not addressed in flowsheet |
| pending_imaging | complete |  |
| pending_labs | complete |  |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Sister to drive patient home after work; window: {'start': '2026-03-16T17:30:00-05:00', 'end': '2026-03-16T18:30:00-05:00'} |
| wound_status | in_progress | detail: Surgical site pain 7/10 despite oral regimen; not yet controlled |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with sister.

**nursing_note**

Slept well overnight. Voiding without difficulty. The patient uses a walking stick at home. They brought it to the hospital. They have been using it during all mobilisation sessions this week and are comfortable with it.

**physician_note**

77-year-old woman with hypertension, osteoarthritis, admitted 3/13 for elective right total knee arthroplasty. Post-op day 2; tolerating diet, voiding.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, tracked_fields.caregiver_status, planned_discharge_window
- B-C06 (single-field) — evidence: tracked_fields.wound_status
- B-F04 (single-field) — evidence: tracked_fields.outpatient_therapy_status

**Information gaps**

- tracked_fields.pending_consult → could indicate B-C04

**Tasks**

- T-CM04 resolves B-S07
- T-RN05 resolves B-C06
- T-CM03 resolves B-F04

**Must not flag (negative controls):** B-C04, B-E05
