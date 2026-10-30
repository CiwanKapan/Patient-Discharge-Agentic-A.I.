# CASE-050 — condition OR

**Planned discharge window:** 2026-06-22T14:00:00-05:00 to 2026-06-22T16:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Daughter will stay with patient for the first week |
| case_manager_status | complete |  |
| diet_education_status | not_applicable |  |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Orthopedic surgery clinic visit booked; scheduled_for: 2026-07-04T16:00:00-05:00 |
| home_health_referral_status | not_applicable |  |
| insurance_authorization_status | in_progress | detail: Prior authorization for crutches and home PT submitted; decision pending |
| medical_device_education_status | in_progress | detail: Continuous passive motion machine teaching started; return demonstration pending |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds; documented_at: 2026-06-21T11:00:00-05:00 |
| medication_availability_status | unknown | detail: Not documented |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | in_progress | detail: Crutches training started; patient not yet safe on stairs |
| outpatient_therapy_status | complete | detail: Outpatient PT referral placed and accepted |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on hip/knee precautions and DVT warning signs completed |
| pcp_notification_status | complete |  |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | complete | detail: Ambulating independently per PT |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Daughter will pick patient up before work; window: {'start': '2026-06-22T08:00:00-05:00', 'end': '2026-06-22T09:00:00-05:00'} |
| wound_status | complete | detail: Incision clean, dry and intact |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Plan is discharge home with daughter.

**nursing_note**

Up in chair for meals. Pain controlled. A routine palliative care screening question was included in the admission assessment as per standard protocol. The patient did not meet the criteria for a palliative care referral. The patient expressed mild anxiety about returning home. This was discussed with the nurse and the social worker. Coping strategies were reviewed. No clinical concern was identified.

**physician_note**

56-year-old woman with obesity, hypertension, admitted 6/18 for left total hip arthroplasty. Post-op day 3; tolerating diet, voiding. 6/22 11:20: Temperature 38.7 C this morning on post-op day 3; source being evaluated.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, planned_discharge_window
- B-C07 (single-field) — evidence: tracked_fields.medical_stability_status, free_text_notes.physician_note
- B-S04 (single-field) — evidence: tracked_fields.insurance_authorization_status
- B-E06 (single-field) — evidence: tracked_fields.medical_device_education_status
- B-E05 (single-field) — evidence: tracked_fields.mobile_device_education_status

**Information gaps**

- tracked_fields.home_safety_status → could indicate B-S03
- tracked_fields.medication_availability_status → could indicate B-E02

**Tasks**

- T-CM04 resolves B-S07
- T-MD04 resolves B-C07 — needs sign-off GR-A07 (escalate_to_attending_physician)
- T-CM06 resolves B-S04
- T-RN08 resolves B-E06
- T-RN07 resolves B-E05

**Must not flag (negative controls):** B-E02, B-S03
