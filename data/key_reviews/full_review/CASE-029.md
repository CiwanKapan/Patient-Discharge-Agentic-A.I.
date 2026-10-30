# CASE-029 — condition HF

**Planned discharge window:** 2026-03-09T11:00:00-05:00 to 2026-03-09T13:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Nephew will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | complete | detail: 2 g sodium and 2 L fluid restriction reviewed with teach-back |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Heart failure clinic visit booked; scheduled_for: 2026-03-13T13:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Telemonitoring scale teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to the hospital outpatient pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-03-08T14:00:00-05:00 |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on daily weights and heart failure symptom monitoring completed |
| pcp_notification_status | not_started | detail: PCP not yet notified of admission or medication changes |
| pending_consult | not_started | detail: Electrophysiology consult ordered; patient not yet seen |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Medical transport to take patient home; window: {'start': '2026-03-09T11:00:00-05:00', 'end': '2026-03-09T12:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with nephew. 3/8 18:00: Metoprolol succinate changed from 25 mg daily to 50 mg daily on evening rounds. Patient and nephew not yet told; this afternoon's teaching covered the old dose. Electrophysiology has not seen the patient yet.

**nursing_note**

Up in chair for meals. Pain controlled. A routine ECG was performed on day 3. The result showed no changes compared to the admission ECG. No clinical action is needed.

**physician_note**

54-year-old man with CAD s/p PCI, CKD stage 3, admitted 3/5 with HFpEF exacerbation precipitated by dietary sodium excess. Net negative 6.8 L this admission; dyspnea back to baseline.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-C04 (single-field) — evidence: tracked_fields.pending_consult
- B-F05 (single-field) — evidence: tracked_fields.pcp_notification_status

**Information gaps**

- tracked_fields.discharge_summary_status → could indicate B-S06

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-MD03 resolves B-C04
- T-CM08 resolves B-F05

**Must not flag (negative controls):** B-S06
