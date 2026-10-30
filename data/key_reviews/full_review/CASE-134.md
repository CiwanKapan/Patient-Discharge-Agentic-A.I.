# CASE-134 — condition CO

**Planned discharge window:** 2026-06-15T08:00:00-05:00 to 2026-06-15T10:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete |  |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Pulmonology clinic visit booked; scheduled_for: 2026-06-27T07:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | in_progress | detail: Peak flow meter teaching started; return demonstration pending |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to Walgreens |
| medication_education_status | complete |  |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | complete | detail: Uses home oxygen 2 L/min at baseline; supply confirmed |
| patient_education_status | complete | detail: Teaching on inhaler technique and the COPD action plan completed |
| pcp_notification_status | not_started | detail: PCP not yet notified of admission or medication changes |
| pending_consult | complete |  |
| pending_imaging | unknown | detail: Not documented |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Medical transport confirmed; window: {'start': '2026-06-16T08:00:00-05:00', 'end': '2026-06-16T09:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with sister.

**nursing_note**

Up in chair for meals. Pain controlled. A mild sleeping tablet was used on the first two nights to help the patient rest. It will not be continued after discharge. This is documented in the discharge plan.

**physician_note**

59-year-old woman with hypertension, former smoker (40 pack-years), admitted 6/9 with COPD exacerbation triggered by viral bronchitis. Ambulated 100 m with PT yesterday without desaturation.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, planned_discharge_window
- B-F05 (single-field) — evidence: tracked_fields.pcp_notification_status
- B-E06 (single-field) — evidence: tracked_fields.medical_device_education_status

**Information gaps**

- tracked_fields.pending_imaging → could indicate B-C03

**Tasks**

- T-CM04 resolves B-S07
- T-CM08 resolves B-F05
- T-RN08 resolves B-E06

**Must not flag (negative controls):** B-C01, B-C03
