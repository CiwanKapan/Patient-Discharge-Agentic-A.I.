# CASE-044 — condition PN

**Planned discharge window:** 2026-05-19T14:00:00-05:00 to 2026-05-19T16:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| case_manager_status | not_started | detail: No case manager assigned to the unit this weekend |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Pulmonology clinic visit booked; scheduled_for: 2026-05-25T16:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete |  |
| medical_stability_status | complete |  |
| medication_availability_status | complete |  |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-05-18T14:00:00-05:00 |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on completing the antibiotic course and pneumonia warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Wife to take patient home; window: {'start': '2026-05-19T15:00:00-05:00', 'end': '2026-05-19T16:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Discharge planning in progress; CM following daily. 5/18 19:00: Per pharmacy, lisinopril changed from 20 mg daily to 10 mg daily. No documentation that the patient or family has been informed of the new dose.

**nursing_note**

Ambulated in hallway with wife present.

**physician_note**

71-year-old man with dementia (mild), type 2 diabetes, admitted 5/14 with left lower lobe pneumonia with small parapneumonic effusion. Oxygen weaned to room air yesterday. The patient practices fasting for religious reasons on certain days of the week. The clinical team was made aware and confirmed this does not conflict with the medication schedule.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-S05 (single-field) — evidence: tracked_fields.case_manager_status

**Information gaps**

- tracked_fields.caregiver_status → could indicate B-F03

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-CM09 resolves B-S05

**Must not flag (negative controls):** B-F03
