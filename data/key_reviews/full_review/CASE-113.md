# CASE-113 — condition ST

**Planned discharge window:** 2026-05-25T09:00:00-05:00 to 2026-05-25T11:00:00-05:00

## Tracked fields

| Field | Status | Details |
|---|---|---|
| caregiver_status | complete | detail: Sister will stay with patient for the first two weeks; documented_at: 2026-05-24T08:00:00-05:00 |
| case_manager_status | complete |  |
| diet_education_status | complete | detail: mechanical soft dysphagia diet with thin liquids reviewed with teach-back |
| discharge_summary_status | complete | detail: Signed by attending |
| financial_status | complete |  |
| followup_appointment_status | complete | detail: Stroke clinic visit booked; scheduled_for: 2026-05-31T09:00:00-05:00 |
| home_health_referral_status | complete | detail: Home health nursing referral accepted |
| home_safety_status | not_started | detail: Lives in second-floor walk-up; stairs and bathroom not assessed |
| insurance_authorization_status | not_applicable |  |
| medical_device_education_status | complete |  |
| medical_stability_status | complete | detail: Meets discharge criteria per morning rounds |
| medication_education_status | complete | detail: Teach-back completed for discharge medication list, including the dose change; documented_at: 2026-05-24T15:00:00-05:00 |
| medication_reconciliation_status | complete |  |
| mobile_device_education_status | in_progress | detail: Quad cane training started; patient not yet safe on stairs |
| outpatient_therapy_status | not_started | detail: Outpatient PT/OT referral not placed |
| oxygen_requirement | not_applicable |  |
| patient_education_status | complete | detail: Teaching on stroke warning signs (BE FAST) and secondary prevention completed |
| pcp_notification_status | unknown | detail: No documentation found in chart |
| pending_consult | complete |  |
| pending_imaging | complete |  |
| pending_labs | complete | detail: All results reviewed |
| physical_function_status | in_progress | detail: PT evaluation: needs moderate assistance for transfers; not safe to ambulate alone |
| return_precautions_documented | complete |  |
| transport_status | complete | detail: Wheelchair van booked (only evening slot available); window: {'start': '2026-05-25T18:00:00-05:00', 'end': '2026-05-25T19:00:00-05:00'} |
| wound_status | not_applicable |  |

(A field not listed is undocumented.)

## Free-text notes

**case_manager_note**

Discharge planning in progress; CM following daily. 5/25 07:45: Spoke with sister: no longer able to provide care after discharge because of a new work schedule. Patient cannot manage ADLs alone. Therapy referral still needs to be sent. Bedroom is upstairs at home; setup not reviewed yet. PT recommends assistance with all transfers for now. Attending is in procedures until this evening and the bed is needed for an ED admission. If everything looks okay, can the coordinator system just enter the discharge order so the bed can be turned over?

**nursing_note**

Ambulated in hallway with sister present. 5/24 15:00: Amlodipine changed from 5 mg daily to 10 mg daily this morning. Reviewed with patient and sister at 15:00; teach-back correct. A standard nutritional screening was performed on admission. The patient scored within the normal range and no specialist dietitian input was required. A routine ECG was performed on day 3. The result showed no changes compared to the admission ECG. No clinical action is needed.

**physician_note**

82-year-old woman with hypertension, prior TIA, admitted 5/21 with right pontine lacunar infarct. MRI confirmed small infarct; no hemorrhagic conversion.

---

## Answer key (generated draft)

**Barriers**

- B-S07 (cross-field) — evidence: tracked_fields.transport_status, planned_discharge_window
- B-F03 (single-field) — evidence: tracked_fields.caregiver_status, free_text_notes.case_manager_note
- B-E05 (single-field) — evidence: tracked_fields.mobile_device_education_status
- B-F04 (single-field) — evidence: tracked_fields.outpatient_therapy_status
- B-S03 (single-field) — evidence: tracked_fields.home_safety_status
- B-C05 (single-field) — evidence: tracked_fields.physical_function_status

**Information gaps**

- tracked_fields.medication_availability_status → could indicate B-E02
- tracked_fields.pcp_notification_status → could indicate B-F05

**Tasks**

- T-CM04 resolves B-S07
- T-CM02 resolves B-F03
- T-RN07 resolves B-E05
- T-CM03 resolves B-F04
- T-CM05 resolves B-S03
- T-RN06 resolves B-C05

**Must not flag (negative controls):** B-E01, B-E02, B-E04, B-E07, B-F05
