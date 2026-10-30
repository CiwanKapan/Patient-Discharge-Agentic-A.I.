# CASE-073 — condition OR

**Planned discharge window:** 2026-04-02T11:00:00-05:00 to 2026-04-02T13:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Sister is primary caregiver; works days, available evenings; window: {'start': '2026-04-02T18:00:00-05:00', 'end': '2026-04-02T22:00:00-05:00'} |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | not_started | detail: Orthopedic surgery clinic follow-up not yet booked |
| home_health_referral_status | not_applicable |  |
| home_safety_status | complete | detail: Single-level home; grab bars installed |
| insurance_authorization_status | complete |  |
| medical_device_education_status | complete | detail: Incision vacuum dressing teaching done with return demonstration |
| medical_stability_status | in_progress | detail: Temperature 38.7 C this morning on post-op day 3; source being evaluated. |
| medication_availability_status | complete | detail: Discharge prescriptions sent to Walgreens |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list, including the dose change; documented_at: 2026-04-01T15:00:00-05:00 |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | complete | detail: Rolling walker training completed with PT |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Sister to drive patient home after work; window: {'start': '2026-04-02T18:30:00-05:00', 'end': '2026-04-02T19:30:00-05:00'} |
| wound_status | complete | detail: Incision clean, dry and intact |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning.

**nursing_note**

Vitals stable this shift. Tolerating diet. Still need to book the orthopedic surgery clinic appointment. 4/1 15:00: Aspirin changed from 81 mg daily to 81 mg twice daily for DVT prophylaxis this morning. Reviewed with patient and sister at 15:00; teach-back correct. The patient had a wisdom tooth extracted under general anaesthetic three years ago with no complications. This is not relevant to the current admission.

**physician_note**

58-year-old man with osteoarthritis, hypothyroidism, admitted 3/27 for ORIF of right bimalleolar ankle fracture. Post-op day 5; working with PT twice daily.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, tracked_fields.caregiver_status, planned_discharge_window
- B-C07 (single-field) — evidence: tracked_fields.medical_stability_status
- B-F01 (single-field) — evidence: tracked_fields.followup_appointment_status

**Information gaps**

- tracked_fields.pending_consult → could indicate B-C04

**Tasks**

- T-CM04 resolves B-S07
- T-MD04 resolves B-C07 — needs sign-off GR-A07 (escalate_to_attending_physician)
- T-CM01 resolves B-F01

**Must not flag (negative controls):** B-C04, B-E01, B-E07
