# CASE-010 — condition OR

**Planned discharge window:** 2026-05-08T11:00:00-05:00 to 2026-05-08T13:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Husband is primary caregiver |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Orthopedic surgery clinic visit booked; scheduled_for: 2026-05-11T12:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | complete | detail: Single-level home; grab bars installed |
| insurance_authorization_status | in_progress | detail: Insurance authorization for short-term rehab placement pending |
| medical_device_education_status | complete |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_availability_status | complete | detail: Discharge prescriptions sent to a local independent pharmacy; documented_at: 2026-05-07T11:00:00-05:00 |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | complete | detail: Knee scooter training completed with PT |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on hip/knee precautions and DVT warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | in_progress | detail: PT evaluation: needs moderate assistance for transfers; not safe to ambulate alone |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Husband to drive patient home; window: {'start': '2026-05-08T11:30:00-05:00', 'end': '2026-05-08T12:30:00-05:00'} |
| wound_status | complete | detail: Incision clean, dry and intact |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with husband. Original evening van slot cancelled; family will drive at the planned discharge time instead.

**nursing_note**

Up in chair for meals. Pain controlled. 5/8 10:00: A local independent pharmacy reports apixaban needs prior authorization; claim rejected, patient cannot pick it up today. PT recommends assistance with all transfers for now. The patient's primary language is not English. A hospital interpreter was present for all key conversations during the stay, including all education sessions. All discharge information was provided in the patient's preferred language.

**physician_note**

85-year-old woman with osteoarthritis, type 2 diabetes, admitted 5/4 for elective right total knee arthroplasty. Post-op day 3; working with PT twice daily.

---

## Answer key (generated draft)

**Barriers**

- B-E02 (single-field) — evidence: tracked_fields.medication_availability_status, free_text_notes.nursing_note
- B-S04 (single-field) — evidence: tracked_fields.insurance_authorization_status
- B-C05 (single-field) — evidence: tracked_fields.physical_function_status

**Information gaps**

- none

**Tasks**

- T-PH03 resolves B-E02
- T-CM06 resolves B-S04
- T-RN06 resolves B-C05

**Must not flag (negative controls):** B-S02, B-S07
