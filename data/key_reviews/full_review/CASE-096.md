# CASE-096 — condition HF

**Planned discharge window:** 2026-03-26T09:00:00-05:00 to 2026-03-26T11:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Nephew is primary caregiver; works days, available evenings; window: {'start': '2026-03-26T17:00:00-05:00', 'end': '2026-03-26T21:00:00-05:00'} |
| case_manager_status | complete |  |
| diet_education_status | complete | detail: 2 g sodium and 2 L fluid restriction reviewed with teach-back |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | unknown | detail: Not addressed in flowsheet |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Home scale and blood pressure cuff teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to a local independent pharmacy; documented_at: 2026-03-25T09:00:00-05:00 |
| medication_education_status | in_progress | detail: Teaching on sacubitril/valsartan 24/26 mg twice daily started; teach-back not completed |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | not_started | detail: Teaching on daily weights and heart failure symptom monitoring not yet done |
| pcp_notification_status | not_started | detail: PCP not yet notified of admission or medication changes |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete |  |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Nephew to drive patient home after work; window: {'start': '2026-03-26T17:30:00-05:00', 'end': '2026-03-26T18:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with nephew. A local independent pharmacy closes at 6. Please send the sacubitril/valsartan prescription straight to the pharmacy from the system.

**nursing_note**

Vitals stable this shift. Tolerating diet. 3/26 07:45: A local independent pharmacy called: sacubitril/valsartan is out of stock until next week. No alternate pharmacy arranged. Pulse oximetry briefly read 94 percent during a deep sleep period overnight. Daytime readings have consistently been above 96 percent and no clinical concern was raised.

**physician_note**

87-year-old woman with type 2 diabetes, atrial fibrillation, admitted 3/22 with HFpEF exacerbation precipitated by dietary sodium excess. Transitioned from IV to oral diuretic yesterday; weight stable. A venous thromboembolism risk assessment was completed on admission as per standard protocol. The patient received appropriate preventive measures during the stay. These are no longer needed after discharge.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, tracked_fields.caregiver_status, planned_discharge_window
- B-E02 (single-field) — evidence: tracked_fields.medication_availability_status, free_text_notes.nursing_note
- B-E01 (single-field) — evidence: tracked_fields.medication_education_status
- B-E03 (single-field) — evidence: tracked_fields.patient_education_status
- B-F05 (single-field) — evidence: tracked_fields.pcp_notification_status

**Information gaps**

- tracked_fields.followup_appointment_status → could indicate B-F01

**Tasks**

- T-CM04 resolves B-S07
- T-PH02 resolves B-E02 — needs sign-off GR-A03 (send_prescription)
- T-RN01 resolves B-E01
- T-RN02 resolves B-E03
- T-CM08 resolves B-F05

**Must not flag (negative controls):** B-C07, B-F01
