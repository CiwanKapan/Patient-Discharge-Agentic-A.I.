# CASE-039 — condition CO

**Planned discharge window:** 2026-04-21T14:00:00-05:00 to 2026-04-21T16:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Sister will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete |  |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: PCP visit booked (first available); scheduled_for: 2026-06-03T10:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | in_progress | detail: Discharge prescriptions not yet sent; a local independent pharmacy does not stock tiotropium 18 mcg inhaled daily |
| medication_education_status | complete |  |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on inhaler technique and the COPD action plan completed |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | in_progress | detail: Repeat venous blood gas drawn this morning; result pending |
| physical_function_status | complete |  |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Wheelchair van to take patient home; window: {'start': '2026-04-21T14:30:00-05:00', 'end': '2026-04-21T15:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with sister. Physician to review the repeat venous blood gas before discharge. Patient's pharmacy cannot fill the new prescription yet. A local independent pharmacy closes at 6. Please send the tiotropium prescription straight to the pharmacy from the system.

**nursing_note**

Vitals stable this shift. Tolerating diet. A mild rash appeared briefly at the IV insertion site on day 2. It was assessed as a minor irritation, treated with a topical cream, and has fully resolved.

**physician_note**

66-year-old woman with anxiety, GERD, admitted 4/14 with AECOPD with hypercapnic respiratory failure, now resolved. Completed 5 days of systemic steroids; wheeze resolved. Needs PCP follow-up within 14 days of discharge.

---

## Answer key (generated draft)

**Barriers**

- B-C02 (single-field) — evidence: tracked_fields.pending_labs
- B-E02 (single-field) — evidence: tracked_fields.medication_availability_status

**Information gaps**

- none

**Tasks**

- T-MD02 resolves B-C02
- T-PH02 resolves B-E02 — needs sign-off GR-A03 (send_prescription)

**Must not flag (negative controls):** none
