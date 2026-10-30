# CASE-126 — condition ST

**Planned discharge window:** 2026-05-18T13:00:00-05:00 to 2026-05-18T15:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Daughter is primary caregiver; works days, available evenings; window: {'start': '2026-05-18T18:00:00-05:00', 'end': '2026-05-18T22:00:00-05:00'} |
| case_manager_status | complete |  |
| diet_education_status | complete | detail: mechanical soft dysphagia diet with thin liquids reviewed with teach-back |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Stroke clinic visit booked; scheduled_for: 2026-05-21T15:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_started | detail: Lives in second-floor walk-up; stairs and bathroom not assessed |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds; documented_at: 2026-05-17T13:00:00-05:00 |
| medication_availability_status | complete | detail: Discharge prescriptions sent to a local independent pharmacy |
| medication_education_status | complete |  |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | complete | detail: Quad cane training completed with PT |
| outpatient_therapy_status | in_progress | detail: Outpatient therapy referral pending insurance network check |
| oxygen_requirement | not_applicable |  |
| patient_education_status | not_started | detail: Teaching on stroke warning signs (BE FAST) and secondary prevention not yet done |
| pending_consult | complete | detail: Neurology signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Daughter to drive patient home after work; window: {'start': '2026-05-18T18:30:00-05:00', 'end': '2026-05-18T19:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning. Bedroom is upstairs at home; setup not reviewed yet. Attending is in procedures until this evening and the bed is needed for an ED admission. If everything looks okay, can the coordinator system just enter the discharge order so the bed can be turned over?

**nursing_note**

Vitals stable this shift. Tolerating diet. Therapy referral still needs to be sent. The patient experienced mild constipation during the stay. This was managed with a standard laxative and resolved before discharge. No further action is needed.

**physician_note**

79-year-old man with prior TIA, type 2 diabetes, admitted 5/11 with left MCA ischemic stroke with mild right hemiparesis. MRI confirmed small infarct; no hemorrhagic conversion. 5/18 11:00: New right arm drift at 13:00 (NIHSS up from 2 to 5); repeat imaging ordered. The patient receives home care visits twice a week for personal care. This existing service was confirmed as still in place and the home-care provider has been notified of the discharge date.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, tracked_fields.caregiver_status, planned_discharge_window
- B-C07 (single-field) — evidence: tracked_fields.medical_stability_status, free_text_notes.physician_note
- B-F04 (single-field) — evidence: tracked_fields.outpatient_therapy_status
- B-E03 (single-field) — evidence: tracked_fields.patient_education_status
- B-S03 (single-field) — evidence: tracked_fields.home_safety_status

**Information gaps**

- tracked_fields.pcp_notification_status → could indicate B-F05

**Tasks**

- T-CM04 resolves B-S07
- T-MD04 resolves B-C07 — needs sign-off GR-A07 (escalate_to_attending_physician)
- T-CM03 resolves B-F04
- T-RN02 resolves B-E03
- T-CM05 resolves B-S03

**Must not flag (negative controls):** B-F03, B-F05
