# CASE-025 — condition ST

**Planned discharge window:** 2026-05-15T13:00:00-05:00 to 2026-05-15T15:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | not_started | detail: No caregiver identified; patient lives alone and needs help with ADLs |
| case_manager_status | complete |  |
| diet_education_status | complete |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Stroke clinic visit booked; scheduled_for: 2026-05-22T14:00:00-05:00 |
| home_health_referral_status | complete |  |
| home_safety_status | in_progress | detail: OT flagged tub shower and no grab bars; modifications not arranged |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to CVS |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-05-14T14:00:00-05:00 |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | complete | detail: Quad cane training completed with PT |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on stroke warning signs (BE FAST) and secondary prevention completed |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | in_progress | detail: Fasting lipid panel drawn this morning; result pending |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning. 5/14 18:00: Atorvastatin changed from 20 mg daily to 80 mg daily on evening rounds. Patient and nephew not yet told; this afternoon's teaching covered the old dose. Physician to review the fasting lipid panel before discharge.

**nursing_note**

Slept well overnight. Voiding without difficulty.

**physician_note**

84-year-old man with hypertension, type 2 diabetes, admitted 5/9 with left thalamic infarct with sensory deficits. MRI confirmed small infarct; no hemorrhagic conversion. The patient experienced mild constipation during the stay. This was managed with a standard laxative and resolved before discharge. No further action is needed. The patient mentioned that they have been stressed at work recently. This was noted. It does not affect the clinical discharge plan and the patient confirmed they feel ready to go home.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-S03 (single-field) — evidence: tracked_fields.home_safety_status
- B-C02 (single-field) — evidence: tracked_fields.pending_labs
- B-F03 (single-field) — evidence: tracked_fields.caregiver_status

**Information gaps**

- tracked_fields.transport_status → could indicate B-S02

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-CM05 resolves B-S03
- T-MD02 resolves B-C02
- T-CM02 resolves B-F03

**Must not flag (negative controls):** B-S02, B-S07
