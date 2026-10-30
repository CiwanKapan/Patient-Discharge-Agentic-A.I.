# CASE-159 — condition CO

**Planned discharge window:** 2026-03-02T14:00:00-05:00 to 2026-03-02T16:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Daughter is primary caregiver |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete |  |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Pulmonology clinic visit booked; scheduled_for: 2026-03-16T14:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_started | detail: Home nebulizer education not completed |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to Walgreens |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-03-01T14:00:00-05:00 |
| medication_reconciliation_status | not_started | detail: Discharge medication reconciliation not yet done |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | complete | detail: Uses home oxygen 2 L/min at baseline; supply confirmed |
| patient_education_status | complete | detail: Teaching on inhaler technique and the COPD action plan completed |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete |  |
| physical_function_status | not_started | detail: Functional assessment not done; patient deconditioned after 5-day stay |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Daughter to drive patient home; window: {'start': '2026-03-02T14:30:00-05:00', 'end': '2026-03-02T15:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning. 3/1 19:00: Prednisone taper: 30 mg x3 days, then 20 mg x3 days, then stop (was 40 mg daily) on evening rounds. Patient and daughter not yet told; this afternoon's teaching covered the old dose. Still waiting on pharmacy to finish the medication reconciliation. Original evening van slot cancelled; family will drive at the planned discharge time instead.

**nursing_note**

Vitals stable this shift. Tolerating diet. The patient lives alone but has confirmed a daily check-in from a neighbour who has agreed to visit each morning. No safety concern was identified.

**physician_note**

67-year-old man with former smoker (40 pack-years), osteoporosis, admitted 2/25 with COPD exacerbation triggered by viral bronchitis. Ambulated 100 m with PT yesterday without desaturation.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-C05 (single-field) — evidence: tracked_fields.physical_function_status
- B-C01 (single-field) — evidence: tracked_fields.medication_reconciliation_status
- B-E06 (single-field) — evidence: tracked_fields.medical_device_education_status

**Information gaps**

- none

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-RN06 resolves B-C05
- T-PH01 resolves B-C01 — needs sign-off GR-A02 (modify_medication_list)
- T-RN08 resolves B-E06

**Must not flag (negative controls):** B-F03, B-S02, B-S07
