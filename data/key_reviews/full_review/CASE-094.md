# CASE-094 — condition ST

**Planned discharge window:** 2026-05-11T12:00:00-05:00 to 2026-05-11T14:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| case_manager_status | complete |  |
| diet_education_status | complete |  |
| discharge_summary_status | in_progress | detail: Discharge summary drafted; not signed |
| financial_status | complete |  |
| followup_appointment_status | unknown | detail: Not documented |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_started | detail: Lives in second-floor walk-up; stairs and bathroom not assessed |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds; documented_at: 2026-05-10T11:00:00-05:00 |
| medication_availability_status | complete | detail: Discharge prescriptions sent to a local independent pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list, including the dose change; documented_at: 2026-05-10T15:00:00-05:00 |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | complete | detail: Quad cane training completed with PT |
| outpatient_therapy_status | complete |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Medical transport confirmed; window: {'start': '2026-05-11T17:00:00-05:00', 'end': '2026-05-11T18:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning. Discharge paperwork still waiting on the summary.

**nursing_note**

Slept well overnight. Voiding without difficulty. 5/10 15:00: Lisinopril changed from 10 mg daily to 20 mg daily this morning. Reviewed with patient and daughter at 15:00; teach-back correct. The patient had a brief episode of a urinary tract infection earlier this year. It was treated with a short course of antibiotics and fully resolved. A screening blood test for thyroid function was added on day 2 as part of a routine check. The result came back normal. No clinical action is required.

**physician_note**

52-year-old man with hypertension, type 2 diabetes, admitted 5/7 with small right cerebellar infarct. MRI confirmed small infarct; no hemorrhagic conversion. 5/11 10:00: BP 214/118 this morning despite oral agents; not at discharge threshold.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, planned_discharge_window
- B-C07 (single-field) — evidence: tracked_fields.medical_stability_status, free_text_notes.physician_note
- B-S06 (single-field) — evidence: tracked_fields.discharge_summary_status
- B-S03 (single-field) — evidence: tracked_fields.home_safety_status

**Information gaps**

- tracked_fields.caregiver_status → could indicate B-F03
- tracked_fields.followup_appointment_status → could indicate B-F01

**Tasks**

- T-CM04 resolves B-S07
- T-MD04 resolves B-C07 — needs sign-off GR-A07 (escalate_to_attending_physician)
- T-MD01 resolves B-S06 — needs sign-off GR-A06 (sign_discharge_summary)
- T-CM05 resolves B-S03

**Must not flag (negative controls):** B-C02, B-E01, B-E07, B-F01, B-F03
