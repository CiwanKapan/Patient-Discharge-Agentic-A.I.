# CASE-160 — condition CO

**Planned discharge window:** 2026-06-15T13:00:00-05:00 to 2026-06-15T15:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete |  |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: PCP visit booked; scheduled_for: 2026-06-22T14:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Peak flow meter teaching done with return demonstration |
| medical_stability_status | in_progress | detail: Desaturating to 84% with ambulation this morning, below baseline; needs re-evaluation before discharge. |
| medication_availability_status | complete | detail: Discharge prescriptions sent to Walgreens |
| medication_education_status | not_started | detail: No teaching yet on new roflumilast 500 mcg daily |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | complete | detail: Uses home oxygen 2 L/min at baseline; supply confirmed |
| patient_education_status | complete | detail: Teaching on inhaler technique and the COPD action plan completed |
| pcp_notification_status | in_progress | detail: Message left with PCP office; no confirmation received |
| pending_consult | complete | detail: Pulmonary rehabilitation signed off |
| pending_imaging | complete |  |
| pending_labs | complete |  |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Son to drive patient home; documented_at: 2026-06-14T11:00:00-05:00; window: {'start': '2026-06-15T13:00:00-05:00', 'end': '2026-06-15T14:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with son. 6/15 10:45: Son called: car broke down, cannot come today. No alternative ride arranged yet.

**nursing_note**

Up in chair for meals. Pain controlled. Need to update the PCP before discharge. A routine falls risk assessment was completed on admission and scored the patient as low risk. No special precautions were required.

**physician_note**

55-year-old man with GERD, osteoporosis, admitted 6/11 with AECOPD with hypercapnic respiratory failure, now resolved. Ambulated 100 m with PT yesterday without desaturation.

---

## Answer key (generated draft)

**Barriers**

- B-S02 (single-field) — evidence: tracked_fields.transport_status, free_text_notes.case_manager_note
- B-F05 (single-field) — evidence: tracked_fields.pcp_notification_status
- B-E01 (single-field) — evidence: tracked_fields.medication_education_status
- B-C07 (single-field) — evidence: tracked_fields.medical_stability_status

**Information gaps**

- none

**Tasks**

- T-CM04 resolves B-S02
- T-CM08 resolves B-F05
- T-RN01 resolves B-E01
- T-MD04 resolves B-C07 — needs sign-off GR-A07 (escalate_to_attending_physician)

**Must not flag (negative controls):** none
