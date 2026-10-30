# CASE-100 — condition OR

**Planned discharge window:** 2026-04-01T09:00:00-05:00 to 2026-04-01T11:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Orthopedic surgery clinic visit booked; scheduled_for: 2026-04-10T08:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | in_progress | detail: OT flagged tub shower and no grab bars; modifications not arranged |
| insurance_authorization_status | complete | detail: DME authorized by insurer |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to CVS |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list; documented_at: 2026-03-31T14:00:00-05:00 |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | complete |  |
| outpatient_therapy_status | in_progress | detail: Outpatient therapy referral pending insurance network check |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on hip/knee precautions and DVT warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | not_started | detail: Internal medicine (co-management) consult ordered; patient not yet seen |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Wife to take patient home; window: {'start': '2026-04-01T09:00:00-05:00', 'end': '2026-04-01T10:00:00-05:00'} |
| wound_status | in_progress | detail: Surgical site pain 7/10 despite oral regimen; not yet controlled |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning. 3/31 18:00: Per pharmacy, aspirin changed from 81 mg daily to 81 mg twice daily for DVT prophylaxis. No documentation that the patient or family has been informed of the new dose. Bedroom is upstairs at home; setup not reviewed yet. Therapy referral still needs to be sent.

**nursing_note**

Vitals stable this shift. Tolerating diet. The patient practices fasting for religious reasons on certain days of the week. The clinical team was made aware and confirmed this does not conflict with the medication schedule.

**physician_note**

63-year-old man with type 2 diabetes, hypertension, admitted 3/25 for left total hip arthroplasty. Post-op day 6; working with PT twice daily. The patient experienced one episode of dizziness when first standing on day 1. This resolved with slow mobilisation guidance from the physiotherapist and has not recurred.

---

## Answer key (generated draft)

**Barriers**

- B-E07 (cross-field) — evidence: tracked_fields.medication_education_status, free_text_notes.case_manager_note
- B-S03 (single-field) — evidence: tracked_fields.home_safety_status
- B-C04 (single-field) — evidence: tracked_fields.pending_consult
- B-F04 (single-field) — evidence: tracked_fields.outpatient_therapy_status
- B-C06 (single-field) — evidence: tracked_fields.wound_status

**Information gaps**

- tracked_fields.caregiver_status → could indicate B-F03

**Tasks**

- T-MD07 resolves B-E07 — needs sign-off GR-A04 (communicate_medication_change_to_patient_or_caregiver)
- T-CM05 resolves B-S03
- T-MD03 resolves B-C04
- T-CM03 resolves B-F04
- T-RN05 resolves B-C06

**Must not flag (negative controls):** B-C07, B-F03
