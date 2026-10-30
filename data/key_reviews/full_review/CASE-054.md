# CASE-054 — condition HF

**Planned discharge window:** 2026-05-11T13:00:00-05:00 to 2026-05-11T15:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Son is primary caregiver; works days, available evenings; window: {'start': '2026-05-11T18:00:00-05:00', 'end': '2026-05-11T22:00:00-05:00'} |
| case_manager_status | complete |  |
| diet_education_status | in_progress | detail: Dietitian visit for 2 g sodium and 2 L fluid restriction scheduled but not completed |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | in_progress | detail: Message sent to heart failure clinic for follow-up; no appointment confirmed |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete |  |
| medication_availability_status | complete |  |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list, including the dose change; documented_at: 2026-05-10T15:00:00-05:00 |
| medication_reconciliation_status | in_progress | detail: Discrepancy between home and inpatient torsemide doses not yet resolved |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on daily weights and heart failure symptom monitoring completed |
| pcp_notification_status | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Son to drive patient home after work; window: {'start': '2026-05-11T18:30:00-05:00', 'end': '2026-05-11T19:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with son.

**nursing_note**

Slept well overnight. Voiding without difficulty. 5/10 15:00: Torsemide changed from 10 mg daily to 20 mg daily this morning. Reviewed with patient and son at 15:00; teach-back correct.

**physician_note**

87-year-old man with type 2 diabetes, CAD s/p PCI, admitted 5/7 with acute decompensated heart failure (EF 30%). Transitioned from IV to oral diuretic yesterday; weight stable. The patient has a history of a kidney stone several years ago. They have had no recurrence since then and this is not relevant to the current admission.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, tracked_fields.caregiver_status, planned_discharge_window
- B-E04 (single-field) — evidence: tracked_fields.diet_education_status
- B-F01 (single-field) — evidence: tracked_fields.followup_appointment_status
- B-C01 (single-field) — evidence: tracked_fields.medication_reconciliation_status

**Information gaps**

- tracked_fields.pending_consult → could indicate B-C04

**Tasks**

- T-CM04 resolves B-S07
- T-RN03 resolves B-E04
- T-CM01 resolves B-F01
- T-PH01 resolves B-C01 — needs sign-off GR-A02 (modify_medication_list)

**Must not flag (negative controls):** B-C04, B-E01, B-E07
