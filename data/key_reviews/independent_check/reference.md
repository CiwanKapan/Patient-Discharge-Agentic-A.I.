# Reference for annotators

This is the taxonomy and the chart-reading rules the systems receive. Use only IDs listed here, and only those whose conditions include the case's condition.

## Barriers

- B-C01 Medication reconciliation incomplete | urgency high | conditions HF,CO,PN,OR,ST | evidence medication_reconciliation_status | cross_field false
  Discharge medication list has not been formally reviewed and reconciled by physician or pharmacist.
- B-C02 Lab/test results pending | urgency high | conditions HF,CO,PN,OR,ST | evidence pending_labs | cross_field false
  Outstanding lab results that have not been reviewed before discharge.
- B-C03 Pending imaging results | urgency high | conditions CO,PN,OR,ST | evidence pending_imaging | cross_field false
  Outstanding imaging or radiology results that have not been reviewed.
- B-C04 Pending specialist consult | urgency high | conditions HF,CO,PN,OR,ST | evidence pending_consult | cross_field false
  A consult was requested and is documented as not yet completed.
- B-C05 Functional or physical limitations | urgency high | conditions HF,CO,PN,OR,ST | evidence physical_function_status | cross_field false
  A clinician or therapist has documented a functional limitation (for example, not safe to ambulate alone) that is not yet addressed.
- B-C06 Wound or surgical site concern | urgency high | conditions OR | evidence wound_status | cross_field false
  The wound or pain assessment is documented as unresolved.
- B-C07 Medical instability | urgency high | conditions HF,CO,PN,OR,ST | evidence medical_stability_status | cross_field false
  A clinician has documented that the patient does not yet meet discharge criteria (stability field or physician note).
- B-E01 New medication not taught | urgency high | conditions HF,CO,PN,OR,ST | evidence medication_education_status | cross_field false
  Patient or caregiver has not been educated on a new or changed medication.
- B-E02 Medication not available | urgency high | conditions HF,CO,PN,OR,ST | evidence medication_availability_status | cross_field false
  Discharge medication will not be available to the patient (delayed prescription, insurance issue, or local pharmacy stock).
- B-E03 Patient education incomplete | urgency high | conditions HF,CO,PN,OR,ST | evidence patient_education_status | cross_field false
  Disease-specific self-management education has not been completed (general education barrier, includes time constraints).
- B-E04 Diet restrictions not taught | urgency high | conditions HF,ST | evidence diet_education_status | cross_field false
  Specific dietary instructions (e.g., 2 g sodium for HF, dysphagia diet for ST) not reviewed.
- B-E05 Mobility device education not done | urgency high | conditions OR,ST | evidence mobile_device_education_status | cross_field false
  Walker, crutches, wheelchair, or other mobility-device education not completed.
- B-E06 Medical device education not done | urgency high | conditions HF,CO,PN,OR,ST | evidence medical_device_education_status | cross_field false
  Education on devices such as glucometers, telemetry boxes, peak flow meters not completed.
- B-E07 Medication change not communicated to patient or caregiver | urgency high | conditions HF,CO,PN,OR,ST | evidence free_text_notes.case_manager_note | cross_field true
  Cross-field / free-text barrier. The medication list was changed during the stay but the patient or caregiver has not been informed. Often surfaces only in nursing or case-manager notes.
- B-F01 Follow-up appointment not scheduled | urgency high | conditions HF,CO,PN,OR,ST | evidence followup_appointment_status | cross_field false
  No post-discharge outpatient appointment booked with PCP, specialist, or clinic.
- B-F03 Lack of caregiver support | urgency high | conditions HF,CO,PN,OR,ST | evidence caregiver_status | cross_field false
  No family member or friend reliably available to help with daily living activities, medication management, or transport.
- B-F04 Outpatient therapy not arranged | urgency medium | conditions OR,ST | evidence outpatient_therapy_status | cross_field false
  Physical therapy, occupational therapy, or speech therapy referral not yet placed.
- B-F05 PCP not notified of discharge | urgency medium | conditions HF,CO,PN,OR,ST | evidence pcp_notification_status | cross_field false
  Primary care provider has not been informed of the hospitalization, medication changes, or follow-up plan.
- B-S01 Financial constraints | urgency high | conditions HF,CO,PN,OR,ST | evidence financial_status | cross_field false
  Out-of-pocket costs for equipment, prescriptions, or skilled-nursing placement create a barrier.
- B-S02 Transportation not arranged | urgency high | conditions HF,CO,PN,OR,ST | evidence transport_status | cross_field false
  No reliable transport home; or transport is unavailable.
- B-S03 Home safety concerns | urgency high | conditions OR,ST | evidence home_safety_status | cross_field false
  A home safety assessment documents an unresolved hazard, or the assessment is documented as not done.
- B-S04 Insurance / prior authorization pending | urgency medium | conditions OR | evidence insurance_authorization_status | cross_field false
  Insurance authorization for required equipment, SNF placement, or medication is pending.
- B-S05 Case manager unavailable | urgency high | conditions HF,CO,PN,OR,ST | evidence case_manager_status | cross_field false
  No case manager available to coordinate post-discharge logistics.
- B-S06 Discharge paperwork pending | urgency high | conditions HF,CO,PN,OR,ST | evidence discharge_summary_status | cross_field false
  Discharge summary is in draft, unsigned, or not reviewed with the patient.
- B-S07 Transport timing conflict | urgency medium | conditions HF,CO,PN,OR,ST | evidence transport_status, planned_discharge_window | cross_field true
  Cross-field barrier. Transport is technically arranged but its available window does not match the planned discharge time (e.g., caregiver only available evenings; discharge planned for morning). If transport is booked but its pickup time, or the planned discharge window, is not documented, the timing cannot be checked: this is an information gap for B-S07 (confirm the pickup time), not a barrier.

## Tasks

- T-MD01 Complete and sign discharge summary | owner_roles physician | resolves B-S06 | conditions HF,CO,PN,OR,ST | urgency high
  Attending physician finalizes and signs the discharge summary including diagnoses, medications, and follow-up plan.
- T-MD02 Review pending labs and imaging | owner_roles physician | resolves B-C02,B-C03 | conditions HF,CO,PN,OR,ST | urgency high
  Physician reviews outstanding lab and radiology results and documents the clinical decision before discharge.
- T-MD03 Complete required specialist consult | owner_roles physician | resolves B-C04 | conditions HF,CO,PN,OR,ST | urgency high
  Ensure required specialist consultations (neurology, cardiology, etc.) are completed and documented.
- T-MD04 Assess and clear medical stability | owner_roles physician | resolves B-C07 | conditions HF,CO,PN,OR,ST | urgency high
  Confirm vital signs, oxygen requirement, and clinical status meet discharge threshold.
- T-MD05 Order home oxygen if required | owner_roles physician | resolves B-C07 | conditions HF,CO,PN | urgency high
  Prescribe and arrange home supplemental oxygen for patients who need it at rest or on exertion.
- T-MD06 Place home-health or PT/OT referral | owner_roles physician | resolves B-C05,B-F04 | conditions HF,CO,OR,ST | urgency high
  Order home-health agency, physical therapy, or occupational therapy service before discharge.
- T-MD07 Communicate medication change to patient or caregiver | owner_roles physician | resolves B-E07 | conditions HF,CO,PN,OR,ST | urgency high
  Physician (or pharmacist) reviews any medication change with the patient or caregiver before discharge.
- T-RN01 Conduct medication education | owner_roles nurse | resolves B-E01 | conditions HF,CO,PN,OR,ST | urgency high
  Nurse educates patient or caregiver on new and changed medications: dose, timing, side effects, and missed-dose action. For a changed medication, this teaching happens only after the change has been communicated under T-MD07 (which needs GR-A04 sign-off), so T-RN01 needs no sign-off of its own.
- T-RN02 Conduct disease-specific patient education | owner_roles nurse | resolves B-E03 | conditions HF,CO,PN,OR,ST | urgency high
  Nurse provides condition-appropriate self-management teaching (daily weights for HF, inhaler technique for COPD, stroke warning signs for ST).
- T-RN03 Teach diet and fluid restrictions | owner_roles nurse | resolves B-E04 | conditions HF,ST | urgency high
  Nurse instructs patient and caregiver on dietary restrictions relevant to the condition.
- T-RN04 Document return precautions | owner_roles nurse | resolves B-E03 | conditions HF,CO,PN,OR,ST | urgency high
  Nurse reviews and documents which symptoms should prompt the patient to return to the ED or call the physician immediately.
- T-RN05 Assess wound and surgical site | owner_roles nurse | resolves B-C06 | conditions OR | urgency high
  Nurse performs final wound assessment, documents status, and provides wound-care instructions.
- T-RN06 Mobility and functional assessment | owner_roles nurse,physical_therapist | resolves B-C05 | conditions HF,CO,PN,OR,ST | urgency high
  Nurse or PT assesses ability to ambulate safely and documents functional status before discharge.
- T-RN07 Mobility device education | owner_roles nurse | resolves B-E05 | conditions OR,ST | urgency high
  Nurse ensures the patient and caregiver know how to use walker, crutches, wheelchair, or similar device safely.
- T-RN08 Medical device education | owner_roles nurse | resolves B-E06 | conditions HF,CO,PN,OR,ST | urgency high
  Nurse ensures the patient or caregiver is educated on devices such as glucometers, telemetry boxes, peak flow meters.
- T-PH01 Complete medication reconciliation | owner_roles pharmacist | resolves B-C01 | conditions HF,CO,PN,OR,ST | urgency high
  Pharmacist reviews the full medication list for duplicates, interactions, omissions, and incorrect doses before discharge.
- T-PH02 Fill discharge prescriptions | owner_roles pharmacist | resolves B-E02 | conditions HF,CO,PN,OR,ST | urgency high
  Pharmacist fills discharge prescriptions in-house so the patient leaves with medications in hand, avoiding community pharmacy delays.
- T-PH03 Obtain prior authorization for medications | owner_roles pharmacist | resolves B-E02,B-S01 | conditions HF,CO,PN,OR,ST | urgency medium
  Pharmacist contacts insurance for prior authorization on high-cost or specialty medications before discharge.
- T-CM01 Schedule follow-up appointment | owner_roles case_manager | resolves B-F01 | conditions HF,CO,PN,OR,ST | urgency high
  Case manager books a post-discharge outpatient appointment.
- T-CM02 Confirm caregiver availability and brief caregiver | owner_roles case_manager,social_worker | resolves B-F03 | conditions HF,CO,PN,OR,ST | urgency high
  Case manager identifies a responsible caregiver, confirms availability, and ensures they are briefed on the care plan.
- T-CM03 Arrange outpatient therapy referrals | owner_roles case_manager | resolves B-F04,B-C05 | conditions OR,ST | urgency medium
  Case manager places referrals for outpatient PT, OT, or speech therapy.
- T-CM04 Arrange patient transport | owner_roles case_manager | resolves B-S02,B-S07 | conditions HF,CO,PN,OR,ST | urgency high
  Case manager arranges reliable transport home, including adjusting timing when there is a conflict with the planned discharge window.
- T-CM05 Conduct home safety assessment | owner_roles case_manager,social_worker | resolves B-S03 | conditions OR,ST | urgency high
  Case manager or social worker evaluates the home environment for fall hazards, accessibility issues, and required modifications.
- T-CM06 Obtain insurance authorization | owner_roles case_manager | resolves B-S04 | conditions OR | urgency medium
  Case manager contacts insurance for authorization for SNF placement, durable medical equipment, or specialized services.
- T-CM07 Connect patient to financial assistance | owner_roles social_worker | resolves B-S01 | conditions HF,CO,PN,OR,ST | urgency medium
  Social worker identifies and connects the patient with financial assistance, Medicaid, Medicare, or community programs.
- T-CM08 Notify primary care provider | owner_roles case_manager | resolves B-F05 | conditions HF,CO,PN,OR,ST | urgency medium
  Case manager or nurse sends the PCP the discharge summary, medication changes, and follow-up plan within 24 hours.
- T-CM09 Assign covering case manager | owner_roles nurse | resolves B-S05 | conditions HF,CO,PN,OR,ST | urgency high
  No case manager is available; the charge nurse requests a covering case manager so post-discharge logistics have an owner before discharge.

## How to read the chart
Each tracked field has a status:
- complete or not_applicable: documented as done or not needed. No barrier from that field alone.
- in_progress or not_started: documented as not done. This is a barrier.
- unknown, or the field is absent: the chart says nothing reliable. This is NOT a barrier. Report it in information_gaps with the barrier it could indicate and the question a human should confirm.

Some barriers only appear when facts are read together (cross_field true in the taxonomy):
- B-S07 transport timing conflict: transport is arranged, but its window does not overlap the planned_discharge_window. Compare the dates and times exactly, including the day. If transport is arranged but its pickup time or the discharge window is not documented, that is an information gap for B-S07, not a barrier.
- B-E07 medication change not communicated: a note documents a medication or dose change after education was recorded, with no record that the patient or caregiver was told.

Free-text notes can also contradict a field that reads complete, for example a physician note saying the patient is not yet stable. Flag those barriers and cite both the field and the note. Notes may also contain distracting details that are documented as resolved or irrelevant; do not flag those.
