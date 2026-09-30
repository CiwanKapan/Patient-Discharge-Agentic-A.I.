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
- **Student Members:** Ciwan Kapan, Julio Clavasquin, Mason McDowell, Dominic
- **Proposal Level:** URECA Team / Scholar Project

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
| 2 | **Case Analyzer** | Parsed Case | Situation Summary | Prevents premature conclusions via structured context. | LLM Reasoning |
| 3 | **Barrier Detector** | Summary | Grounded Barriers | Links every flagged barrier directly to case evidence. | LLM Reasoning |
| 4 | **Task Detector** | Summary | Grounded Tasks | Identifies pending clinical/logistical obligations. | LLM Reasoning |
| 5 | **Rec. Generator** | Barriers & Tasks | Prioritized Actions | Ranks urgent vs. routine recommended next steps. | LLM Reasoning |
| 6 | **Approval Gate** | Proposed Actions | Safety Classification | Deterministically tags: `auto_safe`, `requires_human_approval`, `forbidden`. | Deterministic Code |
| 7 | **Policy Layer** | Proposed Tool Calls | Allowed / Denied | Intercepts forbidden EHR tools (e.g., ordering meds). | Deterministic Code |
| 8 | **Audit Logger** | All Pipeline Events | JSONL Event Trace | Ensures end-to-end traceability and reproducibility (`AU-01` to `AU-08`). | Deterministic Code |

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
2. **Baseline 2 (B2 - Single-Prompt LLM):** Zero-shot LLM operating without external tool access, policy enforcement, or approval gates.

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
│   ├── schemas/
│   │   ├── patient_case_schema.json # JSON Schema for input validation
│   │   └── audit_log_schema.json   # Schema for JSONL audit events
│   ├── synthetic_cases/             # Stratified dataset (160 cases)
│   └── answer_keys/                 # Gold-standard evaluation mappings
├── src/
│   ├── models/                      # Pydantic data models (Case, Audit)
│   ├── pipeline/                    # Pipeline modules 01 through 08
│   ├── tools/                       # Mock allowed (GA-T*) and forbidden (GF-T*) tools
│   └── utils/                       # Append-only JSONL logger
├── baselines/                       # Implementation of B1 and B2 baselines
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
   Create a `.env` file in the root directory and set your API keys if running LLM components:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

---

## 🧪 Running Evaluations & Tests

### Run Pipeline Tests
Execute the pytest suite to verify governance gates, policy interception, and component validation:
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
- **Immutable Audit Trail (`AU-01` to `AU-08`):** Every case run generates a complete event trace in JSONL format for auditability and compliance reporting.

---

