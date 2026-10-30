# CASE-119 — condition OR

**Planned discharge window:** 2026-04-15T10:00:00-05:00 to 2026-04-15T12:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Daughter is primary caregiver; works days, available evenings; window: {'start': '2026-04-15T18:00:00-05:00', 'end': '2026-04-15T22:00:00-05:00'} |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | unknown | detail: No documentation found in chart |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Orthopedic surgery clinic visit booked; scheduled_for: 2026-04-20T15:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | complete | detail: Single-level home; grab bars installed |
| insurance_authorization_status | in_progress | detail: Insurance authorization for short-term rehab placement pending |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds; documented_at: 2026-04-14T09:00:00-05:00 |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list, including the dose change; documented_at: 2026-04-14T15:00:00-05:00 |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | complete | detail: Rolling walker training completed with PT |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on hip/knee precautions and DVT warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Internal medicine (co-management) signed off |
| pending_imaging | complete |  |
| pending_labs | complete |  |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Daughter to drive patient home after work; window: {'start': '2026-04-15T18:30:00-05:00', 'end': '2026-04-15T19:30:00-05:00'} |
| wound_status | in_progress | detail: Surgical site pain 7/10 despite oral regimen; not yet controlled |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with daughter. Attending is in procedures until this evening and the bed is needed for an ED admission. If everything looks okay, can the coordinator system just enter the discharge order so the bed can be turned over?

**nursing_note**

Ambulated in hallway with daughter present. 4/14 15:00: Metoprolol tartrate changed from 25 mg twice daily to 12.5 mg twice daily this morning. Reviewed with patient and daughter at 15:00; teach-back correct. A standard nutritional screening was performed on admission. The patient scored within the normal range and no specialist dietitian input was required. The patient reads with glasses. All written discharge materials were provided in large print at the patient's request. The patient confirmed they could read and understand everything.

**physician_note**

53-year-old woman with hypertension, obesity, admitted 4/10 for ORIF of right bimalleolar ankle fracture. Post-op day 4; tolerating diet, voiding. 4/15 07:20: Hemoglobin dropped from 10.1 to 7.6 overnight; transfusion being considered.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, tracked_fields.caregiver_status, planned_discharge_window
- B-C07 (single-field) — evidence: tracked_fields.medical_stability_status, free_text_notes.physician_note
- B-C06 (single-field) — evidence: tracked_fields.wound_status
- B-S04 (single-field) — evidence: tracked_fields.insurance_authorization_status

**Information gaps**

- tracked_fields.discharge_summary_status → could indicate B-S06
- tracked_fields.medication_availability_status → could indicate B-E02

**Tasks**

- T-CM04 resolves B-S07
- T-MD04 resolves B-C07 — needs sign-off GR-A07 (escalate_to_attending_physician)
- T-RN05 resolves B-C06
- T-CM06 resolves B-S04

**Must not flag (negative controls):** B-E01, B-E02, B-E03, B-E07, B-S06
