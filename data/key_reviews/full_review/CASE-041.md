# CASE-041 — condition PN

**Planned discharge window:** 2026-04-29T09:00:00-05:00 to 2026-04-29T11:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Daughter is primary caregiver |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Pulmonology clinic visit booked; scheduled_for: 2026-05-02T09:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to CVS; documented_at: 2026-04-28T06:00:00-05:00 |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | in_progress | detail: Pharmacist started reconciliation; home list from outside pharmacy not yet reviewed |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Speech-language pathology (swallow) signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Daughter to drive patient home; window: {'start': '2026-04-29T09:30:00-05:00', 'end': '2026-04-29T10:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and daughter to review the discharge plan. Earlier pickup was cancelled and rebooked for 09:30 to match the discharge time.

**nursing_note**

Vitals stable this shift. Tolerating diet. 4/29 07:00: CVS reports cefpodoxime needs prior authorization; claim rejected, patient cannot pick it up today. The patient had a previous hospital admission for the same condition eighteen months ago. That episode was fully resolved and is not relevant to the current discharge plan.

**physician_note**

80-year-old woman with hypertension, alcohol use disorder in remission, admitted 4/24 with multilobar community-acquired pneumonia. Oxygen weaned to room air yesterday.

---

## Answer key (generated draft)

**Barriers**

- B-E02 (single-field) — evidence: tracked_fields.medication_availability_status, free_text_notes.nursing_note
- B-C01 (single-field) — evidence: tracked_fields.medication_reconciliation_status

**Information gaps**

- none

**Tasks**

- T-PH03 resolves B-E02
- T-PH01 resolves B-C01 — needs sign-off GR-A02 (modify_medication_list)

**Must not flag (negative controls):** B-S02, B-S07
