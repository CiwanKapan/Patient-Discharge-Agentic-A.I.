# Patient-Discharge-Agentic-A.I.

## 📌 Project Overview

Hospital discharge represents a critical care transition where incomplete information and unaddressed barriers frequently lead to preventable 30-day readmissions. While agentic AI offers a promising mechanism for multi-step reasoning and task execution, evaluating these systems requires a rigorous, offline benchmark before any live clinical deployment.

This project implements and evaluates a **supervised agentic AI discharge coordinator** designed to:
- Decompose complex patient cases into structured clinical and social summaries.
- Identify grounded discharge barriers and pending tasks using a closed taxonomy.
- Execute mock clinical tool calls under strict deterministic governance.
- Enforce approval gates for high-risk operations.
- Maintain an immutable, append-only JSONL audit log.

The primary objective is to evaluate whether a supervised agentic architecture outperforms static rule-based and single-prompt LLM baselines in barrier detection, task assignment, plan completeness, and governance compliance.

---

## 👥 Project Team & Mentorship

- **Project Mentor:** Khem Poudel
- **Student Members:** Ciwan Kapan, Julio Clavasquin, Mason McDowell, Dominic Zeferin
- **Project:** URECA Team Project

---

## 🔬 Research Question & Hypotheses

**Research Question (RQ):**  
*Can a supervised agentic AI coordinator identify discharge barriers and pending tasks more accurately, produce more complete discharge plans, and follow governance rules more reliably than non-agentic baselines in an offline setting?*

| Hypothesis | Description | Target Performance |
| :--- | :--- | :--- |
| **H1 (Barrier Recall)** | Agentic AI > Baselines | Higher recall in identifying grounded barriers |
| **H2 (Task Recall)** | Agentic AI > Baselines | Higher recall in identifying pending obligations |
| **H3 (Plan Completeness)** | Agentic AI > Baselines | Superior coverage of discharge plan components |
| **H4 (Governance Compliance)** | Agentic AI > Baselines | **Large effect size expected** (100% adherence to safety controls) |

---

## ⚙️ Architecture & AI Workflow

The system is structured as an 8-stage pipeline with strict deterministic governance wrapper layers surrounding the LLM reasoning modules.

```
       ┌─────────────────────────┐
       │   Patient Chart JSON    │
       └────────────┬────────────┘
                    │
       ┌────────────▼────────────┐       ┌─────────────────────────┐
       │  1. Input Reader        ├───────┼─►                       │
       └────────────┬────────────┘       │                         │
       ┌────────────▼────────────┐       │                         │
       │  2. Case Analyzer       ├───────┼─►                       │
       └────────────┬────────────┘       │                         │
          ┌─────────┴─────────┐          │                         │
       ┌──▼──────────┐   ┌────▼────────┐ │                         │
       │3. Barrier   │   │4. Task      ├─┼─►   8. Audit Logger     │
       │   Detector  │   │   Detector  │ │    (Append-only JSONL)  │
       └──┬──────────┘   └────┬────────┘ │                         │
          └─────────┬─────────┘          │                         │
       ┌────────────▼────────────┐       │                         │
       │  5. Rec. Generator      ├───────┼─►                       │
       └────────────┬────────────┘       │                         │
          ┌─────────┴─────────┐          │                         │
       ┌──▼──────────┐   ┌────▼────────┐ │                         │
       │6. Approval  │   │7. Policy    ├─┼─────────────────────────┘
       │   Gate      │   │   Layer     │ │
       └──┬──────────┘   └────┬────────┘ │
          └─────────┬─────────┘          │
       ┌────────────▼────────────┐       │
       │  Output Composer        ├───────┘
       └────────────┬────────────┘
                    │
       ┌────────────▼────────────┐
       │ Discharge Recommendation│
       └─────────────────────────┘
```

### Modular Component Breakdown

| # | Module | Input | Output | Safety & Governance Role | Type |
|---|---|---|---|---|---|
| 1 | **Input Reader** | Raw Case JSON | Validated Object | Schema validation; fails loudly on malformed data. | Deterministic Code |
| 2 | **Case Analyzer** | Parsed Case | `AgentMessage[CaseSummary]` | Prevents premature conclusions via structured context. | LLM Reasoning |
| 3 | **Barrier Detector** | `CaseSummary` | `AgentMessage[BarrierDetection]` | Links every flagged barrier directly to case evidence. | LLM Reasoning |
| 4 | **Task Detector** | `CaseSummary` + `BarrierDetection` | `AgentMessage[TaskDetection]` | Identifies pending clinical/logistical obligations. | LLM Reasoning |
| 5 | **Rec. Generator** | Barriers, Gaps & Tasks | `AgentMessage[RecommendationSet]` | Ranks urgent vs. routine recommended next steps. | LLM Reasoning |
| 6 | **Approval Gate** | `RecommendationSet` | `AgentMessage[ApprovalDecisions]` | Deterministically tags: `auto_safe`, `requires_human_approval`, `forbidden`. | Deterministic Code |
| 7 | **Policy Layer** | `ToolCall` requests | `AgentMessage[PolicyLayerOutput]` | Intercepts forbidden EHR tools (e.g., ordering meds). | Deterministic Code |
| 8 | **Audit Logger** | All Pipeline Events | `AuditEvent` JSONL lines | Ensures end-to-end traceability and reproducibility (`AU-01` to `AU-08`). | Deterministic Code |

### Inter-Agent Message Contract

Every stage hands off the same envelope, `AgentMessage`, defined in `src/models/messages.py`. Only the `payload` type changes between stages. This keeps integration and troubleshooting uniform: any output can be traced to the run, stage, model, prompt version, and upstream messages that produced it.

| Envelope field | Purpose |
|---|---|
| `schema_version` | Contract version (currently `1.0`). |
| `message_id`, `upstream` | This message's ID and the IDs of the messages it was built from. |
| `run_id`, `case_id`, `stage` | Which run, case, and pipeline stage produced it. |
| `model`, `prompt_version` | Set for LLM stages, `null` for deterministic code. |
| `payload` | The stage's output type, listed below. The stage must match the payload type. |
| `warnings` | Non-fatal issues raised by the stage. |

| Stage | Payload | Defined in |
|---|---|---|
| 02 Case Analyzer | `CaseSummary` | `src/models/messages.py` |
| 03 Barrier Detector | `BarrierDetection` | `src/models/messages.py` |
| 04 Task Detector | `TaskDetection` | `src/models/messages.py` |
| 05 Rec. Generator | `RecommendationSet` | `src/models/plan.py` |
| 06 Approval Gate | `ApprovalDecisions` | `src/models/plan.py` |
| 07 Policy Layer | `PolicyLayerOutput` | `src/models/tools.py` |
| 08 Output Composer | `DischargePlan` | `src/models/plan.py` |

Contract rules:
- **Every finding cites evidence.** Each barrier and task carries `evidence` entries that point at a case path, such as `tracked_fields.transport_status` or `free_text_notes.case_manager_note`.
- **Cross-field barriers cite two or more fields.** A barrier marked `cross_field: true` is rejected unless it points at at least two distinct fields.
- **Taxonomy checks.** `check_against_taxonomy()` confirms IDs exist and fit the condition, that `cross_field` matches the taxonomy, and that each task resolves a barrier that was actually flagged.
- **No silent repair.** LLM output that fails validation is rejected and logged.
- **Recommendations are either tasks or checks.** A `complete_task` recommendation names a task and the barriers it resolves. A `verify_information` recommendation names an information gap and claims no barrier.
- **Approval classifications are consistent.** `requires_human_approval` is true exactly when the classification says so, and it must cite a `GR-A*` rule. A `forbidden` classification must cite a `GF-T*` tool. `check_governance()` confirms every approval-required action was classified correctly.
- **Proposing is not calling.** Some names are both an approval-required action and a forbidden tool, such as `modify_medication_list`. Proposing the action for a clinician needs approval. Calling the tool is always forbidden.
- **Default deny for tools.** The policy layer allows only tools on the `GA-T*` list. Forbidden tools and unknown tools are denied, and tool results exist only for allowed calls. `check_policy()` verifies each decision against the taxonomy.

The Pydantic models are the source of truth. JSON Schemas in `data/schemas/` are generated from them with `python scripts/export_schemas.py`, and a test fails if the committed schemas are out of date.

### Missing Information vs. Incomplete Tasks

The case schema separates "documented as not done" from "not documented". Each tracked field in `tracked_fields` has an explicit `status`:

| Status | Meaning | Reading | Result |
|---|---|---|---|
| `complete` | Documented as done | satisfied | No barrier |
| `not_applicable` | Documented as not needed | satisfied | No barrier |
| `in_progress` | Started, not finished | incomplete | Barrier |
| `not_started` | Documented as not done | incomplete | Barrier |
| `unknown` or field omitted | The chart says nothing reliable | missing | **Information gap** |

An information gap is reported in `BarrierDetection.information_gaps`, not in `barriers`. It names the field, the barrier it *could* indicate, and the question a human should confirm. It becomes a verification action rather than a discharge barrier. For example, a follow-up appointment that is not documented is an information gap for `B-F01`. A follow-up documented as `not_started` is the `B-F01` barrier itself.

Answer keys mirror this split with `information_gaps` and a `must_not_flag` list of negative controls. Flagging a barrier where the key expects an information gap is counted as a **gap misflag**, a false positive reported separately in the metrics.

### Cross-Field Evaluation Scenarios

Some barriers only appear when fields are read together. `B-S07` (transport timing conflict) is the clearest case: transport is arranged and every field looks fine on its own, but the pickup window does not overlap the planned discharge window. Time-bound items carry a `window`, and the case carries a top-level `planned_discharge_window`, so these relationships can be checked.

`data/scenarios/` holds small hand-built cases with answer keys that isolate this reasoning:

| Scenario | What it tests | Expected |
|---|---|---|
| `SCN-XF-01` | Van booked for the evening, discharge planned for the morning | `B-S07` |
| `SCN-XF-02` | Same clock times, but pickup is booked for the next day | `B-S07` |
| `SCN-XF-03` | Caregiver driver is only available in the evening | `B-S07` |
| `SCN-XF-04` | Teaching documented complete, then a later note shows a dose change | `B-E07` |
| `SCN-XF-NEG-01` | Pickup window sits inside the discharge window | No barrier (negative control) |
| `SCN-XF-NEG-02` | Note mentions a cancelled early pickup, rebooked pickup fits | No barrier (negative control) |
| `SCN-MI-01` | Transport arranged, but no pickup time documented | Information gap for `B-S07` |
| `SCN-MI-02` | Follow-up appointment not documented | Information gap for `B-F01` |
| `SCN-MI-03` | Follow-up documented as not booked | `B-F01` |
| `SCN-MI-04` | Lab status explicitly marked unknown | Information gap for `B-C02` |

`tests/test_scenarios.py` verifies each answer key against deterministic field readings. It confirms that every field cited by a cross-field barrier reads as satisfied on its own, so the barrier can only be found by comparing fields. `evaluation/metrics.py` reports these slices next to overall precision and recall:

- **`cross_field_recall`** is recall on barriers that need two or more fields read together.
- **`information_gap_recall`** is how many undocumented items the system asked about instead of ignoring.
- **`gap_misflags`** counts barriers flagged where the information was only missing.
- **`negative_control_hits`** counts flags on barriers listed in `must_not_flag`.

---

## 📊 Dataset & Baseline Specifications

### Dataset Structure
- **Size:** 160 synthetic cases paired with independently authored expert answer keys.
- **Stratification:** Easy, Medium, and Hard difficulty levels across 5 medical conditions:
  - Heart Failure (`HF`)
  - COPD (`CO`)
  - Pneumonia (`PN`)
  - Post-Surgical Orthopedic (`OR`)
  - Stroke (`ST`)
- **Distractors:** Integrates up to 140 standardized distractor phrases across 7 clinical/social themes to test AI over-flagging and precision.
- **Privacy & IRB:** 100% synthetic data with **zero HIPAA/IRB privacy risk**.

### Experimental Baselines
1. **Baseline 1 (B1 - Rule-Based):** Static, hard-coded checklist performing field validation without semantic reasoning.
2. **Baseline 2 (B2 - Single-Prompt LLM):** Zero-shot LLM (Claude Haiku 5.5) operating without external tool access, policy enforcement, or approval gates.

---

## 📁 Repository Structure

```
agentic_discharge_coordinator/
├── README.md
├── requirements.txt
├── config/
│   ├── taxonomy.json                # Closed taxonomy (Barriers, Tasks, Governance IDs)
│   └── distractors.json             # Distractor phrase reference repository
├── data/
│   ├── schemas/                     # Generated from src/models (scripts/export_schemas.py)
│   │   ├── patient_case_schema.json # JSON Schema for input validation
│   │   ├── answer_key_schema.json   # Gold-standard answer key format
│   │   ├── scenario_schema.json     # Targeted scenario (case + key) format
│   │   ├── tool_call_schema.json    # Tool call request format
│   │   ├── messages/                # Inter-agent message schemas (stages 02-08)
│   │   └── audit_log_schema.json   # Schema for JSONL audit events
│   ├── scenarios/                   # Targeted cross-field and missing-info scenarios
│   ├── synthetic_cases/             # Stratified dataset (160 cases)
│   └── answer_keys/                 # Gold-standard evaluation mappings
├── src/
│   ├── models/                      # Pydantic models: case, inter-agent messages, answer keys, audit
│   ├── pipeline/                    # Pipeline modules 01 through 08
│   ├── tools/                       # Mock allowed (GA-T*) and forbidden (GF-T*) tools
│   └── utils/                       # Append-only JSONL logger, deterministic case checks
├── baselines/                       # Implementation of B1 and B2 baselines
├── scripts/
│   ├── build_config.py              # Builds config/*.json from the source .docx files
│   └── export_schemas.py            # Regenerates data/schemas/*.json from src/models
├── evaluation/                      # Evaluation suite and hypothesis metric scripts
└── tests/                           # Unit tests for policy layer & pipeline stages
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- Git

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-org/agentic-discharge-coordinator.git
   cd agentic-discharge-coordinator
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup:**
   Create a `.env` file in the root directory and set your Anthropic API key if running LLM components. All LLM stages and Baseline 2 use Claude Haiku 5.5:
   ```env
   ANTHROPIC_API_KEY=your_api_key_here
   CLAUDE_MODEL=claude-haiku-5-5
   ```

---

## 🛠️ Building the Config Files

`config/taxonomy.json` and `config/distractors.json` are generated from the team's source Word documents. Do not edit the JSON by hand; update the `.docx` sources and rebuild:

```bash
python scripts/build_config.py <taxonomy.docx> <distractors.docx> config/
```

The script checks ID integrity (no duplicates, every task resolves a known barrier, every distractor references a valid barrier) and prints the entry counts plus any corrections it applied to the source.

---

## 🧪 Running Evaluations & Tests

### Run Pipeline Tests
Execute the pytest suite to verify governance gates, policy interception, component validation, the inter-agent contracts, and the targeted scenarios:
```bash
pytest tests/
```

### Run Baseline Comparison & Evaluation Suite
Run the full benchmark script against the 160 synthetic cases:
```bash
python evaluation/evaluate.py --all-baselines --dataset data/synthetic_cases/
```

---

## 🛡️ Governance & Security Highlights

This system is built with a **human-in-the-loop (HITL)** architecture and deterministic security controls:
- **Forbidden Tools (`GF-T01` to `GF-T06`):** Any attempt by the LLM to call clinical write functions (e.g., placing discharge orders or sending prescriptions) is intercepted and logged as a policy denial.
- **Approval-Required Actions (`GR-A01` to `GR-A07`):** High-stakes recommendations must carry the `requires_human_approval = true` flag.
- **Immutable Audit Trail (`AU-01` to `AU-08`):** Every case run generates a complete event trace in JSONL format for auditability and compliance reporting. Each line is an `AuditEvent` from `src/models/audit.py` with a typed `details` object per event type. `check_audit_trail()` verifies that a run starts with `case_loaded`, ends with `run_completed`, and has unbroken sequence numbers. It also confirms every tool call has a policy decision and that the logged barriers, tasks, approvals, and denials match the emitted plan. A run whose plan has no barriers, tasks, or actions is not penalized for the matching events it could not log. For tool calls, the `run_completed` event records how many calls the policy layer reviewed, and the number of logged tool call and policy decision events must match it. A count of zero is the only way a run may log no tool calls, so a dropped event is caught instead of looking like a run without calls.

---

