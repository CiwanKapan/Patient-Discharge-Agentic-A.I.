# CASE-083 — condition CO

**Planned discharge window:** 2026-06-19T08:00:00-05:00 to 2026-06-19T10:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Son is primary caregiver; works days, available evenings; window: {'start': '2026-06-19T17:00:00-05:00', 'end': '2026-06-19T21:00:00-05:00'} |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete |  |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Pulmonology clinic visit rebooked at patient request; scheduled_for: 2026-07-03T10:00:00-05:00 |
| home_health_referral_status | complete |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Home nebulizer teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to a local independent pharmacy |
| medication_education_status | not_started | detail: No teaching yet on new tiotropium 18 mcg inhaled daily |
| medication_reconciliation_status | not_started | detail: Discharge medication reconciliation not yet done |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | complete | detail: Uses home oxygen 2 L/min at baseline; supply confirmed |
| patient_education_status | complete | detail: Teaching on inhaler technique and the COPD action plan completed |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | not_started | detail: Functional assessment not done; patient deconditioned after 4-day stay |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Son to drive patient home after work; window: {'start': '2026-06-19T17:30:00-05:00', 'end': '2026-06-19T18:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and son to review the discharge plan. Patient asked to move the pulmonology clinic appointment; rebooked within 14 days of discharge.

**nursing_note**

Ambulated in hallway with son present. Still waiting on pharmacy to finish the medication reconciliation. Patient asked what the new tiotropium 18 mcg inhaled daily is for; teaching still needed. A mild rash appeared briefly at the IV insertion site on day 2. It was assessed as a minor irritation, treated with a topical cream, and has fully resolved.

**physician_note**

63-year-old woman with former smoker (40 pack-years), GERD, admitted 6/15 with COPD exacerbation triggered by viral bronchitis. Ambulated 100 m with PT yesterday without desaturation.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, tracked_fields.caregiver_status, planned_discharge_window
- B-C01 (single-field) — evidence: tracked_fields.medication_reconciliation_status
- B-E01 (single-field) — evidence: tracked_fields.medication_education_status
- B-C05 (single-field) — evidence: tracked_fields.physical_function_status

**Information gaps**

- none

**Tasks**

- T-CM04 resolves B-S07
- T-PH01 resolves B-C01 — needs sign-off GR-A02 (modify_medication_list)
- T-RN01 resolves B-E01
- T-RN06 resolves B-C05

**Must not flag (negative controls):** B-F01
