# CASE-009 — condition OR

**Planned discharge window:** 2026-06-05T09:00:00-05:00 to 2026-06-05T11:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Daughter is primary caregiver |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| home_health_referral_status | not_applicable |  |
| home_safety_status | complete | detail: Single-level home; grab bars installed |
| insurance_authorization_status | complete | detail: DME authorized by insurer |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to the hospital outpatient pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-06-04T14:00:00-05:00 |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | complete |  |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | not_started | detail: PCP not yet notified of admission or medication changes |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Daughter to drive patient home; window: {'start': '2026-06-05T09:30:00-05:00', 'end': '2026-06-05T10:30:00-05:00'} |
| wound_status | complete | detail: Incision clean, dry and intact |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with daughter. 6/4 18:00: Per pharmacy, oxycodone changed from 5 mg every 4 hours as needed to 5 mg every 6 hours as needed, 5-day supply. No documentation that the patient or family has been informed of the new dose. Need to update the PCP before discharge. Daughter normally works days but has taken the afternoon off to drive the patient home at the planned time.

**nursing_note**

Vitals stable this shift. Tolerating diet. A mild rash appeared briefly at the IV insertion site on day 2. It was assessed as a minor irritation, treated with a topical cream, and has fully resolved.

**physician_note**

60-year-old woman with hypothyroidism, hypertension, admitted 6/2 for left total hip arthroplasty. Post-op day 2; pain controlled on oral regimen.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-F05 (single-field) — evidence: tracked_fields.pcp_notification_status

**Information gaps**

- tracked_fields.followup_appointment_status → could indicate B-F01

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-CM08 resolves B-F05

**Must not flag (negative controls):** B-F01, B-S02, B-S07
