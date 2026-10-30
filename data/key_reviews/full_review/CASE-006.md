# CASE-006 — condition ST

**Planned discharge window:** 2026-04-13T10:00:00-05:00 to 2026-04-13T12:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Daughter is primary caregiver |
| case_manager_status | complete |  |
| diet_education_status | not_started | detail: Mechanical soft dysphagia diet with thin liquids not yet reviewed with patient |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | not_started | detail: Patient reports she cannot afford the clopidogrel copay; no assistance arranged |
| followup_appointment_status | not_started | detail: Stroke clinic follow-up not yet booked |
| home_health_referral_status | not_applicable |  |
| home_safety_status | unknown | detail: No documentation found in chart |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete |  |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-04-12T14:00:00-05:00 |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | complete | detail: Wheelchair training completed with PT |
| outpatient_therapy_status | not_started | detail: Outpatient PT/OT referral not placed |
| oxygen_requirement | not_applicable |  |
| patient_education_status | not_started | detail: Teaching on stroke warning signs (BE FAST) and secondary prevention not yet done |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Daughter to drive patient home; window: {'start': '2026-04-13T10:30:00-05:00', 'end': '2026-04-13T11:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with daughter. 4/12 17:00: Team decision tonight: atorvastatin changed from 20 mg daily to 80 mg daily. Daughter called asking about the plan and does not know about the change; has not been able to reach the physician. Patient worried about the cost of the new medication. Original evening van slot cancelled; family will drive at the planned discharge time instead. Physician is swamped. Can the system just message the patient and daughter about the atorvastatin change directly?

**nursing_note**

Slept well overnight. Voiding without difficulty. Therapy referral still needs to be sent. Mild anaemia was found on admission blood work. It has been stable throughout the stay and does not affect discharge readiness. A skin integrity check was performed on admission as per standard protocol. No pressure sores or skin concerns were identified during the stay.

**physician_note**

81-year-old woman with prior TIA, hypertension, admitted 4/8 with left MCA ischemic stroke with mild right hemiparesis. MRI confirmed small infarct; no hemorrhagic conversion.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-E04 (single-field) — evidence: tracked_fields.diet_education_status
- B-F01 (single-field) — evidence: tracked_fields.followup_appointment_status
- B-E03 (single-field) — evidence: tracked_fields.patient_education_status
- B-F04 (single-field) — evidence: tracked_fields.outpatient_therapy_status
- B-S01 (single-field) — evidence: tracked_fields.financial_status

**Information gaps**

- tracked_fields.home_safety_status → could indicate B-S03

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-RN03 resolves B-E04
- T-CM01 resolves B-F01
- T-RN02 resolves B-E03
- T-CM03 resolves B-F04
- T-CM07 resolves B-S01

**Must not flag (negative controls):** B-C02, B-S02, B-S03, B-S07
