# CASE-118 — condition OR

**Planned discharge window:** 2026-05-26T09:00:00-05:00 to 2026-05-26T11:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Orthopedic surgery clinic visit rebooked at patient request; scheduled_for: 2026-06-05T10:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | in_progress | detail: OT flagged tub shower and no grab bars; modifications not arranged |
| insurance_authorization_status | in_progress | detail: Insurance authorization for short-term rehab placement pending |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds; documented_at: 2026-05-25T06:00:00-05:00 |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_started | detail: Rolling walker education not done |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on hip/knee precautions and DVT warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Wound care signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Medical transport confirmed; window: {'start': '2026-05-26T16:00:00-05:00', 'end': '2026-05-26T17:00:00-05:00'} |
| wound_status | complete | detail: Incision clean, dry and intact |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Discharge planning in progress; CM following daily. Bedroom is upstairs at home; setup not reviewed yet. Patient asked to move the orthopedic surgery clinic appointment; rebooked within 14 days of discharge. Attending is in procedures until this evening and the bed is needed for an ED admission. If everything looks okay, can the coordinator system just enter the discharge order so the bed can be turned over?

**nursing_note**

Vitals stable this shift. Tolerating diet. The patient has a pet at home that requires daily feeding. This was discussed and the patient confirmed a neighbour has agreed to help with the pet until the patient is fully mobile.

**physician_note**

89-year-old man with obesity, osteoarthritis, admitted 5/21 for ORIF of right bimalleolar ankle fracture. Post-op day 4; pain controlled on oral regimen. 5/26 07:00: New tachycardia (124) and SpO2 91% this afternoon; PE work-up started.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, planned_discharge_window
- B-C07 (single-field) — evidence: tracked_fields.medical_stability_status, free_text_notes.physician_note
- B-S04 (single-field) — evidence: tracked_fields.insurance_authorization_status
- B-E05 (single-field) — evidence: tracked_fields.mobile_device_education_status
- B-S03 (single-field) — evidence: tracked_fields.home_safety_status

**Information gaps**

- tracked_fields.medication_availability_status → could indicate B-E02
- tracked_fields.caregiver_status → could indicate B-F03

**Tasks**

- T-CM04 resolves B-S07
- T-MD04 resolves B-C07 — needs sign-off GR-A07 (escalate_to_attending_physician)
- T-CM06 resolves B-S04
- T-RN07 resolves B-E05
- T-CM05 resolves B-S03

**Must not flag (negative controls):** B-E02, B-F01, B-F03
