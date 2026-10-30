# CASE-005 — condition HF

**Planned discharge window:** 2026-06-12T15:00:00-05:00 to 2026-06-12T17:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | not_started | detail: No caregiver identified; patient lives alone and needs help with ADLs |
| case_manager_status | complete |  |
| diet_education_status | complete | detail: 2 g sodium and 2 L fluid restriction reviewed with teach-back |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: PCP visit booked (first available); scheduled_for: 2026-07-06T09:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_applicable |  |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | not_applicable |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to a local independent pharmacy |
| medication_education_status | complete |  |
| medication_reconciliation_status | complete | detail: Reconciled by pharmacist |
| mobile_device_education_status | not_applicable |  |
| outpatient_therapy_status | not_applicable |  |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete |  |
| pcp_notification_status | complete |  |
| pending_consult | complete | detail: Cardiology signed off |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Medical transport booked by CM |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Discharge planning in progress; CM following daily. Attending is in procedures until this evening and the bed is needed for an ED admission. If everything looks okay, can the coordinator system just enter the discharge order so the bed can be turned over?

**nursing_note**

Up in chair for meals. Pain controlled. A standard nutritional screening was performed on admission. The patient scored within the normal range and no specialist dietitian input was required.

**physician_note**

61-year-old man with atrial fibrillation, type 2 diabetes, admitted 6/8 with HFpEF exacerbation precipitated by dietary sodium excess. Diuresed 6 kg with IV furosemide; now euvolemic on oral regimen. Needs PCP follow-up within 7 days of discharge.

---

## Answer key (generated draft)

**Barriers**

- B-F03 (single-field) — evidence: tracked_fields.caregiver_status

**Information gaps**

- tracked_fields.transport_status → could indicate B-S07

**Tasks**

- T-CM02 resolves B-F03

**Must not flag (negative controls):** B-E04, B-S07
