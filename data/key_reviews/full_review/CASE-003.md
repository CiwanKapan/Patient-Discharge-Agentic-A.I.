# CASE-003 — condition HF

**Planned discharge window:** 2026-05-20T14:00:00-05:00 to 2026-05-20T16:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Daughter will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | complete | detail: 2 g sodium and 2 L fluid restriction reviewed with teach-back |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Cardiology clinic visit booked; scheduled_for: 2026-05-25T15:00:00-05:00 |
| home_health_referral_status | complete |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | in_progress | detail: Home scale and blood pressure cuff teaching started; return demonstration pending |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds; documented_at: 2026-05-19T11:00:00-05:00 |
| medication_availability_status | unknown | detail: No documentation found in chart |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | not_started | detail: Discharge medication reconciliation not yet done |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on daily weights and heart failure symptom monitoring completed |
| pcp_notification_status | unknown | detail: Not addressed in flowsheet |
| pending_consult | complete | detail: Nephrology signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Wheelchair van booked; window: {'start': '2026-05-20T07:00:00-05:00', 'end': '2026-05-20T08:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with daughter.

**nursing_note**

Slept well overnight. Voiding without difficulty. Still waiting on pharmacy to finish the medication reconciliation.

**physician_note**

75-year-old woman with CAD s/p PCI, hypertension, admitted 5/15 with acute on chronic HFrEF exacerbation with volume overload. Transitioned from IV to oral diuretic yesterday; weight stable. 5/20 11:45: Symptomatic hypotension (84/50) this morning after dose increase; reassessing. The patient had a fractured wrist five years ago that healed completely. No ongoing treatment is needed and this does not affect the current plan. A routine review of the patient's long-term conditions was completed by the attending physician. No new diagnoses were made and no changes to ongoing management were recommended.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, planned_discharge_window
- B-C07 (single-field) — evidence: tracked_fields.medical_stability_status, free_text_notes.physician_note
- B-C01 (single-field) — evidence: tracked_fields.medication_reconciliation_status
- B-E06 (single-field) — evidence: tracked_fields.medical_device_education_status

**Information gaps**

- tracked_fields.pcp_notification_status → could indicate B-F05
- tracked_fields.medication_availability_status → could indicate B-E02

**Tasks**

- T-CM04 resolves B-S07
- T-MD04 resolves B-C07 — needs sign-off GR-A07 (escalate_to_attending_physician)
- T-PH01 resolves B-C01 — needs sign-off GR-A02 (modify_medication_list)
- T-RN08 resolves B-E06

**Must not flag (negative controls):** B-E02, B-F05
