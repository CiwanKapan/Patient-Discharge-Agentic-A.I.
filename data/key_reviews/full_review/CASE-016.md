# CASE-016 — condition HF

**Planned discharge window:** 2026-03-03T13:00:00-05:00 to 2026-03-03T15:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Wife will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | complete |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: PCP visit booked; scheduled_for: 2026-03-06T14:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to CVS; documented_at: 2026-03-02T10:00:00-05:00 |
| medication_education_status | complete |  |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on daily weights and heart failure symptom monitoring completed |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Cardiology signed off |
| pending_imaging | complete |  |
| pending_labs | in_progress | detail: Repeat BNP resulted overnight but not yet reviewed by physician |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Wife to take patient home; window: {'start': '2026-03-03T13:30:00-05:00', 'end': '2026-03-03T14:30:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with wife.

**nursing_note**

Up in chair for meals. Pain controlled. 3/3 11:00: CVS called: sacubitril/valsartan is out of stock until next week. No alternate pharmacy arranged. The patient had a cataract removed from one eye two years ago. The result was successful. Vision in both eyes is stable and this has no current clinical significance.

**physician_note**

53-year-old man with atrial fibrillation, hypertension, admitted 2/27 with new-onset heart failure with reduced ejection fraction. Net negative 3.0 L this admission; dyspnea back to baseline.

---

## Answer key (generated draft)

**Barriers**

- B-E02 (single-field) — evidence: tracked_fields.medication_availability_status, free_text_notes.nursing_note
- B-C02 (single-field) — evidence: tracked_fields.pending_labs

**Information gaps**

- none

**Tasks**

- T-PH02 resolves B-E02 — needs sign-off GR-A03 (send_prescription)
- T-MD02 resolves B-C02

**Must not flag (negative controls):** none
