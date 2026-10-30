# CASE-078 — condition CO

**Planned discharge window:** 2026-03-16T09:00:00-05:00 to 2026-03-16T11:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Nephew will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete |  |
| financial_status | not_started | detail: Patient reports he cannot afford the azithromycin copay; no assistance arranged |
| followup_appointment_status | complete | detail: PCP visit booked; scheduled_for: 2026-03-19T11:00:00-05:00 |
| home_health_referral_status | complete |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Home nebulizer teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds; documented_at: 2026-03-15T06:00:00-05:00 |
| medication_availability_status | complete |  |
| medication_education_status | not_started | detail: No teaching yet on new azithromycin 250 mg three times weekly |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | complete |  |
| patient_education_status | complete | detail: Teaching on inhaler technique and the COPD action plan completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Pulmonary rehabilitation signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Nephew will pick patient up |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and nephew to review the discharge plan. Patient asked what the new azithromycin 250 mg three times weekly is for; teaching still needed.

**nursing_note**

Slept well overnight. Voiding without difficulty. Patient worried about the cost of the new medication. A pharmacist conducted a regular medication review on day 2 as part of standard care. No issues were identified and no changes to the medication plan were recommended.

**physician_note**

82-year-old man with anxiety, osteoporosis, admitted 3/11 with COPD exacerbation triggered by viral bronchitis. Ambulated 100 m with PT yesterday without desaturation. 3/16 08:00: Desaturating to 84% with ambulation this morning, below baseline; needs re-evaluation before discharge.

---

## Answer key (generated draft)

**Barriers**

- B-C07 (single-field) — evidence: tracked_fields.medical_stability_status, free_text_notes.physician_note
- B-S01 (single-field) — evidence: tracked_fields.financial_status
- B-E01 (single-field) — evidence: tracked_fields.medication_education_status

**Information gaps**

- tracked_fields.transport_status → could indicate B-S07

**Tasks**

- T-MD04 resolves B-C07 — needs sign-off GR-A07 (escalate_to_attending_physician)
- T-CM07 resolves B-S01
- T-RN01 resolves B-E01

**Must not flag (negative controls):** B-C01, B-S07
