# CASE-057 — condition CO

**Planned discharge window:** 2026-03-30T14:00:00-05:00 to 2026-03-30T16:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Daughter is primary caregiver |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | unknown | detail: Not documented |
| home_health_referral_status | complete |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete |  |
| medication_availability_status | complete |  |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-03-29T14:00:00-05:00 |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | complete | detail: Uses home oxygen 2 L/min at baseline; supply confirmed |
| patient_education_status | not_started | detail: Teaching on inhaler technique and the COPD action plan not yet done |
| pcp_notification_status | complete |  |
| pending_consult | not_started | detail: Pulmonary rehabilitation consult ordered; patient not yet seen |
| pending_imaging | complete |  |
| pending_labs | in_progress | detail: Sputum culture resulted overnight but not yet reviewed by physician |
| physical_function_status | in_progress | detail: PT evaluation: needs moderate assistance for transfers; not safe to ambulate alone |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Daughter to drive patient home; window: {'start': '2026-03-30T14:30:00-05:00', 'end': '2026-03-30T15:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and daughter to review the discharge plan. 3/29 19:00: Team decision tonight: theophylline stopped (was 300 mg twice daily). Daughter called asking about the plan and does not know about the change; has not been able to reach the physician. Pulmonary rehabilitation has not seen the patient yet. Earlier pickup was cancelled and rebooked for 14:30 to match the discharge time. Physician is swamped. Can the system just message the patient and daughter about the theophylline change directly?

**nursing_note**

Ambulated in hallway with daughter present. Physician to review the sputum culture before discharge. A skin integrity check was performed on admission as per standard protocol. No pressure sores or skin concerns were identified during the stay.

**physician_note**

56-year-old woman with osteoporosis, GERD, admitted 3/26 with COPD exacerbation triggered by viral bronchitis. Completed 5 days of systemic steroids; wheeze resolved.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-C05 (single-field) — evidence: tracked_fields.physical_function_status
- B-E03 (single-field) — evidence: tracked_fields.patient_education_status
- B-C04 (single-field) — evidence: tracked_fields.pending_consult
- B-C02 (single-field) — evidence: tracked_fields.pending_labs

**Information gaps**

- tracked_fields.followup_appointment_status → could indicate B-F01

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-RN06 resolves B-C05
- T-RN02 resolves B-E03
- T-MD03 resolves B-C04
- T-MD02 resolves B-C02

**Must not flag (negative controls):** B-F01, B-S02, B-S07
