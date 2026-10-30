# CASE-098 — condition OR

**Planned discharge window:** 2026-06-16T13:00:00-05:00 to 2026-06-16T15:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Husband is primary caregiver; works days, available evenings; window: {'start': '2026-06-16T17:00:00-05:00', 'end': '2026-06-16T21:00:00-05:00'} |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete |  |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Orthopedic surgery clinic visit booked; scheduled_for: 2026-06-28T13:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | complete | detail: Single-level home; grab bars installed |
| insurance_authorization_status | in_progress | detail: Insurance authorization for short-term rehab placement pending |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to CVS |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | complete | detail: Crutches training completed with PT |
| outpatient_therapy_status | complete |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on hip/knee precautions and DVT warning signs completed |
| pcp_notification_status | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Husband to drive patient home after work; window: {'start': '2026-06-16T17:30:00-05:00', 'end': '2026-06-16T18:30:00-05:00'} |
| wound_status | in_progress | detail: Incision with new serous drainage and surrounding erythema; wound team to reassess |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with husband.

**nursing_note**

Ambulated in hallway with husband present.

**physician_note**

67-year-old woman with hypothyroidism, osteoarthritis, admitted 6/12 for ORIF of right bimalleolar ankle fracture. Post-op day 3; working with PT twice daily. A routine review of the patient's long-term conditions was completed by the attending physician. No new diagnoses were made and no changes to ongoing management were recommended.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, tracked_fields.caregiver_status, planned_discharge_window
- B-C06 (single-field) — evidence: tracked_fields.wound_status
- B-S04 (single-field) — evidence: tracked_fields.insurance_authorization_status

**Information gaps**

- tracked_fields.pending_consult → could indicate B-C04

**Tasks**

- T-CM04 resolves B-S07
- T-RN05 resolves B-C06
- T-CM06 resolves B-S04

**Must not flag (negative controls):** B-C04
