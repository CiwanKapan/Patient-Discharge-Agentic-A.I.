# CASE-084 — condition HF

**Planned discharge window:** 2026-04-06T11:00:00-05:00 to 2026-04-06T13:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Son is primary caregiver |
| case_manager_status | complete |  |
| diet_education_status | in_progress | detail: Dietitian visit for 2 g sodium and 2 L fluid restriction scheduled but not completed |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: PCP visit booked (first available); scheduled_for: 2026-05-05T09:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete | detail: Home scale and blood pressure cuff teaching done with return demonstration |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to the hospital outpatient pharmacy |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list, including the dose change; documented_at: 2026-04-05T15:00:00-05:00 |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on daily weights and heart failure symptom monitoring completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Nephrology signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Son to drive patient home; window: {'start': '2026-04-06T11:30:00-05:00', 'end': '2026-04-06T12:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

CM following for discharge planning. Patient has questions about what to eat at home. Original evening van slot cancelled; family will drive at the planned discharge time instead.

**nursing_note**

Vitals stable this shift. Tolerating diet. 4/5 15:00: Metoprolol succinate changed from 25 mg daily to 50 mg daily this morning. Reviewed with patient and son at 15:00; teach-back correct. The patient had a cataract removed from one eye two years ago. The result was successful. Vision in both eyes is stable and this has no current clinical significance.

**physician_note**

79-year-old woman with type 2 diabetes, hypertension, admitted 3/30 with acute on chronic HFrEF exacerbation with volume overload. Transitioned from IV to oral diuretic yesterday; weight stable. Needs PCP follow-up within 7 days of discharge.

---

## Answer key (generated draft)

**Barriers**

- B-E04 (single-field) — evidence: tracked_fields.diet_education_status

**Information gaps**

- none

**Tasks**

- T-RN03 resolves B-E04

**Must not flag (negative controls):** B-E01, B-E07, B-S02, B-S07
