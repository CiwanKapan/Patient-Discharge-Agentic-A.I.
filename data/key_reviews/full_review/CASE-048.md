# CASE-048 — condition HF

**Planned discharge window:** 2026-05-27T09:00:00-05:00 to 2026-05-27T11:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Son is primary caregiver; works days, available evenings; window: {'start': '2026-05-27T17:00:00-05:00', 'end': '2026-05-27T21:00:00-05:00'} |
| case_manager_status | complete |  |
| diet_education_status | complete |  |
| discharge_summary_status | complete |  |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Heart failure clinic visit rebooked at patient request; scheduled_for: 2026-06-03T10:00:00-05:00 |
| home_health_referral_status | complete |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete |  |
| medication_availability_status | complete | detail: Discharge prescriptions sent to CVS; documented_at: 2026-05-26T07:00:00-05:00 |
| medication_education_status | in_progress | detail: Teaching on sacubitril/valsartan 24/26 mg twice daily started; teach-back not completed |
| medication_reconciliation_status | unknown | detail: No documentation found in chart |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | in_progress | detail: Teaching on daily weights and heart failure symptom monitoring started; patient asked for son to be present for the rest |
| pcp_notification_status | complete |  |
| pending_consult | in_progress | detail: Cardiology consult requested yesterday; recommendations not yet documented |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | not_started | detail: Functional assessment not done; patient deconditioned after 5-day stay |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Son to drive patient home after work; window: {'start': '2026-05-27T17:30:00-05:00', 'end': '2026-05-27T18:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning. Patient asked to move the heart failure clinic appointment; rebooked within 7 days of discharge.

**nursing_note**

Vitals stable this shift. Tolerating diet. 5/27 07:00: CVS reports sacubitril/valsartan needs prior authorization; claim rejected, patient cannot pick it up today. PT recommends assistance with all transfers for now. Patient asked what the new sacubitril/valsartan 24/26 mg twice daily is for; teaching still needed. A venous thromboembolism risk assessment was completed on admission as per standard protocol. The patient received appropriate preventive measures during the stay. These are no longer needed after discharge. Mild swelling was noted in the patient's ankles on examination. This is an expected baseline finding for this condition and is not a new or worsening problem.

**physician_note**

73-year-old woman with CAD s/p PCI, CKD stage 3, admitted 5/22 with acute decompensated heart failure (EF 30%). Transitioned from IV to oral diuretic yesterday; weight stable.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, tracked_fields.caregiver_status, planned_discharge_window
- B-E02 (single-field) — evidence: tracked_fields.medication_availability_status, free_text_notes.nursing_note
- B-C04 (single-field) — evidence: tracked_fields.pending_consult
- B-C05 (single-field) — evidence: tracked_fields.physical_function_status
- B-E03 (single-field) — evidence: tracked_fields.patient_education_status
- B-E01 (single-field) — evidence: tracked_fields.medication_education_status

**Information gaps**

- tracked_fields.medication_reconciliation_status → could indicate B-C01

**Tasks**

- T-CM04 resolves B-S07
- T-PH03 resolves B-E02
- T-MD03 resolves B-C04
- T-RN06 resolves B-C05
- T-RN02 resolves B-E03
- T-RN01 resolves B-E01

**Must not flag (negative controls):** B-C01, B-C07, B-F01
