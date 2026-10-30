# CASE-117 — condition OR

**Planned discharge window:** 2026-05-04T15:00:00-05:00 to 2026-05-04T17:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Sister will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Orthopedic surgery clinic visit booked; scheduled_for: 2026-05-12T15:00:00-05:00 |
| home_health_referral_status | complete |  |
| home_safety_status | complete | detail: Single-level home; grab bars installed |
| insurance_authorization_status | in_progress | detail: Prior authorization for crutches and home PT submitted; decision pending |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to the hospital outpatient pharmacy; documented_at: 2026-05-03T14:00:00-05:00 |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | complete | detail: Crutches training completed with PT |
| outpatient_therapy_status | complete |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on hip/knee precautions and DVT warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Wheelchair van to take patient home; window: {'start': '2026-05-04T15:30:00-05:00', 'end': '2026-05-04T16:30:00-05:00'} |
| wound_status | in_progress | detail: Surgical site pain 7/10 despite oral regimen; not yet controlled |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with sister.

**nursing_note**

Vitals stable this shift. Tolerating diet. 5/4 13:20: The hospital outpatient pharmacy reports apixaban needs prior authorization; claim rejected, patient cannot pick it up today.

**physician_note**

79-year-old man with osteoarthritis, type 2 diabetes, admitted 4/29 for ORIF of right bimalleolar ankle fracture. Post-op day 4; working with PT twice daily. The patient has a close friend who visits weekly and helps with shopping. This was noted as a positive social support factor. No concerns were raised about the patient's social situation.

---

## Answer key (generated draft)

**Barriers**

- B-E02 (single-field) — evidence: tracked_fields.medication_availability_status, free_text_notes.nursing_note
- B-S04 (single-field) — evidence: tracked_fields.insurance_authorization_status
- B-C06 (single-field) — evidence: tracked_fields.wound_status

**Information gaps**

- none

**Tasks**

- T-PH03 resolves B-E02
- T-CM06 resolves B-S04
- T-RN05 resolves B-C06

**Must not flag (negative controls):** B-F03
