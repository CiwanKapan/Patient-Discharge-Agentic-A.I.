# CASE-046 — condition OR

**Planned discharge window:** 2026-05-26T11:00:00-05:00 to 2026-05-26T13:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Son is primary caregiver |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | in_progress | detail: Discharge summary about 60% complete |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Orthopedic surgery clinic visit rebooked at patient request; scheduled_for: 2026-06-09T10:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | complete |  |
| insurance_authorization_status | in_progress | detail: Insurance authorization for short-term rehab placement pending |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to CVS |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-05-25T14:00:00-05:00 |
| medication_reconciliation_status | in_progress | detail: Discrepancy between home and inpatient metoprolol tartrate doses not yet resolved |
| mobile_device_education_status | complete | detail: Crutches training completed with PT |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on hip/knee precautions and DVT warning signs completed |
| pcp_notification_status | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Son to drive patient home; window: {'start': '2026-05-26T11:30:00-05:00', 'end': '2026-05-26T12:30:00-05:00'} |
| wound_status | in_progress | detail: Surgical site pain 7/10 despite oral regimen; not yet controlled |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Met with patient and son to review the discharge plan. 5/25 19:00: Team decision tonight: metoprolol tartrate changed from 25 mg twice daily to 12.5 mg twice daily. Son called asking about the plan and does not know about the change; has not been able to reach the physician. Still waiting on pharmacy to finish the medication reconciliation. Original evening van slot cancelled; family will drive at the planned discharge time instead. Patient asked to move the orthopedic surgery clinic appointment; rebooked within 14 days of discharge.

**nursing_note**

Vitals stable this shift. Tolerating diet. The patient reads with glasses. All written discharge materials were provided in large print at the patient's request. The patient confirmed they could read and understand everything.

**physician_note**

56-year-old man with type 2 diabetes, hypertension, admitted 5/19 for ORIF of right bimalleolar ankle fracture. Post-op day 6; working with PT twice daily.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-S04 (single-field) — evidence: tracked_fields.insurance_authorization_status
- B-S06 (single-field) — evidence: tracked_fields.discharge_summary_status
- B-C01 (single-field) — evidence: tracked_fields.medication_reconciliation_status
- B-C06 (single-field) — evidence: tracked_fields.wound_status

**Information gaps**

- tracked_fields.pending_consult → could indicate B-C04

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-CM06 resolves B-S04
- T-MD01 resolves B-S06 — needs sign-off GR-A06 (sign_discharge_summary)
- T-PH01 resolves B-C01 — needs sign-off GR-A02 (modify_medication_list)
- T-RN05 resolves B-C06

**Must not flag (negative controls):** B-C04, B-E03, B-F01, B-S02, B-S07
