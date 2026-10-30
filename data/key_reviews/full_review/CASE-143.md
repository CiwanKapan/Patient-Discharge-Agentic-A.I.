# CASE-143 — condition CO

**Planned discharge window:** 2026-06-01T15:00:00-05:00 to 2026-06-01T17:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Sister is primary caregiver |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: PCP visit booked; scheduled_for: 2026-06-11T14:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | in_progress | detail: Discharge prescriptions not yet sent; the hospital outpatient pharmacy does not stock tiotropium 18 mcg inhaled daily |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-05-31T14:00:00-05:00 |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on inhaler technique and the COPD action plan completed |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | in_progress | detail: Repeat venous blood gas resulted overnight but not yet reviewed by physician |
| physical_function_status | in_progress | detail: PT evaluation: needs moderate assistance for transfers; not safe to ambulate alone |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Sister to drive patient home; window: {'start': '2026-06-01T15:30:00-05:00', 'end': '2026-06-01T16:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with sister. 5/31 17:00: Per pharmacy, budesonide/formoterol switched to fluticasone/umeclidinium/vilanterol one inhalation daily (was 160/4.5 two puffs twice daily). No documentation that the patient or family has been informed of the new dose. Sister normally works days but has taken the afternoon off to drive the patient home at the planned time. The hospital outpatient pharmacy closes at 6. Please send the tiotropium prescription straight to the pharmacy from the system.

**nursing_note**

Vitals stable this shift. Tolerating diet. PT recommends assistance with all transfers for now. The patient has a long-standing history of mild hearing loss that is managed with a hearing aid. They have their own hearing aid at home and this does not affect the discharge plan.

**physician_note**

80-year-old man with osteoporosis, former smoker (40 pack-years), admitted 5/27 with COPD exacerbation triggered by viral bronchitis. Weaned from BiPAP on day 2; now on room air at rest.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-C05 (single-field) — evidence: tracked_fields.physical_function_status
- B-E02 (single-field) — evidence: tracked_fields.medication_availability_status
- B-C02 (single-field) — evidence: tracked_fields.pending_labs

**Information gaps**

- tracked_fields.pcp_notification_status → could indicate B-F05

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-RN06 resolves B-C05
- T-PH02 resolves B-E02 — needs sign-off GR-A03 (send_prescription)
- T-MD02 resolves B-C02

**Must not flag (negative controls):** B-F05, B-S02, B-S07
