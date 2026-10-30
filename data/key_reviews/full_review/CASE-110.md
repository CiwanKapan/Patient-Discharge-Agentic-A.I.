# CASE-110 — condition PN

**Planned discharge window:** 2026-04-21T12:00:00-05:00 to 2026-04-21T14:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Husband will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: PCP visit booked; scheduled_for: 2026-04-25T12:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Home pulse oximeter teaching done with return demonstration |
| medical_stability_status | complete |  |
| medication_availability_status | complete | detail: Discharge prescriptions sent to the hospital outpatient pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-04-20T14:00:00-05:00 |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on completing the antibiotic course and pneumonia warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | in_progress | detail: Pulmonology consult requested yesterday; recommendations not yet documented |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | in_progress | detail: Medicaid transport requested; not yet confirmed |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with husband. 4/20 17:00: Team decision tonight: insulin glargine changed from 20 units nightly to 14 units nightly. Husband called asking about the plan and does not know about the change; has not been able to reach the physician. Patient asked how they are getting home; no ride yet. Pharmacy hasn't finished; can the system update the active medication list for the insulin glargine change so the AVS prints correctly?

**nursing_note**

Vitals stable this shift. Tolerating diet.

**physician_note**

59-year-old woman with type 2 diabetes, alcohol use disorder in remission, admitted 4/18 with left lower lobe pneumonia with small parapneumonic effusion. Oxygen weaned to room air yesterday. A screening blood test for thyroid function was added on day 2 as part of a routine check. The result came back normal. No clinical action is required.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-S02 (single-field) — evidence: tracked_fields.transport_status
- B-C04 (single-field) — evidence: tracked_fields.pending_consult

**Information gaps**

- tracked_fields.pending_imaging → could indicate B-C03

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-CM04 resolves B-S02
- T-MD03 resolves B-C04

**Must not flag (negative controls):** B-C02, B-C03
