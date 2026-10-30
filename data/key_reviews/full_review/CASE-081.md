# CASE-081 — condition PN

**Planned discharge window:** 2026-03-06T11:00:00-05:00 to 2026-03-06T13:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Son is primary caregiver |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: PCP visit rebooked at patient request; scheduled_for: 2026-03-11T10:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Incentive spirometer teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | not_started | detail: Levofloxacin 750 mg daily x3 days needs prior authorization; not available at a local independent pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-03-05T14:00:00-05:00 |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | not_started | detail: Teaching on completing the antibiotic course and pneumonia warning signs not yet done |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Pulmonology signed off |
| pending_imaging | complete |  |
| pending_labs | unknown | detail: No documentation found in chart |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Son to drive patient home; window: {'start': '2026-03-06T11:30:00-05:00', 'end': '2026-03-06T12:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with son. 3/5 18:00: Team decision tonight: metformin held until follow-up (was 1000 mg twice daily). Son called asking about the plan and does not know about the change; has not been able to reach the physician. Patient's pharmacy cannot fill the new prescription yet. Original evening van slot cancelled; family will drive at the planned discharge time instead. Patient asked to move the PCP appointment; rebooked within 7 days of discharge.

**nursing_note**

Vitals stable this shift. Tolerating diet. A chest X-ray taken on admission showed mild changes. A repeat X-ray on day 3 shows significant improvement and the radiologist has cleared the patient for discharge.

**physician_note**

56-year-old woman with hypertension, dementia (mild), admitted 2/28 with left lower lobe pneumonia with small parapneumonic effusion. Leukocytosis resolved; tolerating diet.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-E02 (single-field) — evidence: tracked_fields.medication_availability_status
- B-E03 (single-field) — evidence: tracked_fields.patient_education_status

**Information gaps**

- tracked_fields.pending_labs → could indicate B-C02

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-PH03 resolves B-E02
- T-RN02 resolves B-E03

**Must not flag (negative controls):** B-C02, B-C03, B-F01, B-S02, B-S07
