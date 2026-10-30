# CASE-087 — condition CO

**Planned discharge window:** 2026-04-02T09:00:00-05:00 to 2026-04-02T11:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Sister will stay with patient for the first week |
| case_manager_status | not_started | detail: No case manager assigned to the unit this weekend |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Pulmonology clinic visit booked (first available); scheduled_for: 2026-05-14T10:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Home nebulizer teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | unknown | detail: Not addressed in flowsheet |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | complete | detail: Uses home oxygen 2 L/min at baseline; supply confirmed |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Pulmonary rehabilitation signed off |
| pending_imaging | in_progress | detail: Repeat chest X-ray completed; awaiting radiology read |
| pending_labs | complete |  |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | not_started | detail: No ride home arranged; patient does not drive |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with sister.

**nursing_note**

Slept well overnight. Voiding without difficulty.

**physician_note**

88-year-old woman with hypertension, osteoporosis, admitted 3/29 with AECOPD with hypercapnic respiratory failure, now resolved. Ambulated 100 m with PT yesterday without desaturation. Needs pulmonology clinic follow-up within 14 days of discharge. Oxygen saturation briefly dipped to 93 percent during a period of exertion on day 2. The patient was rested and saturation returned to 97 percent. No change to the oxygen plan was needed.

---

## Answer key (generated draft)

**Barriers**

- B-S05 (single-field) — evidence: tracked_fields.case_manager_status
- B-S02 (single-field) — evidence: tracked_fields.transport_status
- B-C03 (single-field) — evidence: tracked_fields.pending_imaging

**Information gaps**

- tracked_fields.medication_availability_status → could indicate B-E02

**Tasks**

- T-CM09 resolves B-S05
- T-CM04 resolves B-S02
- T-MD02 resolves B-C03

**Must not flag (negative controls):** B-C07, B-E02
