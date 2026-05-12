# 🛡️ Cyber‑Nexus: Self-Evolving AI Security Agent

Cyber‑Nexus is a cloud‑native autonomous security agent that defends Linux systems against advanced persistent threats (APT), prompt injection, and multi‑turn adversarial attacks.

Built on top of fine‑tuned open‑source LLMs with a dual‑system cognitive architecture and a fully automated red‑team/blue‑team evolution loop.

## 🧠 Core Architecture

| System | Role | Response Time |
|--------|------|---------------|
| **System 1** | Fast, intuitive defense against routine commands and known attack patterns | < 1 second |
| **System 2** | Deep simulation and deliberation in a sandboxed RL environment | Triggered when confidence is low |

### Continuous Evolution Loop

Red Team Attack → Blue Team Defense → Failure Analysis → Auto Data Curation → Incremental Fine‑tuning → New Version Release

## 🚀 Key Features

- Fine‑tuned Qwen3‑8B Student model via LoRA (distilled from Qwen3‑30B Teacher)
- Structured security audits in `[思考]...[行动] JSON` format
- Automated red‑team / blue‑team arena with cognitive auditing
- AST‑level semantic analysis for deobfuscation and APT simulation
- Expected Value (EV) driven risk assessment for ambiguous instructions
- Regression gate to prevent catastrophic forgetting during evolution

## 📂 Repository Structure

├── README.md
├── docs/
├── scripts/
│   ├── teacher/
│   ├── student/
│   └── arena/
└── assets/

## 🏗️ Tech Stack

- **Base Model:** Qwen3‑8B (Student), Qwen3‑30B‑A3B (Teacher)
- **Fine‑tuning:** LoRA (rank=64) + BFloat16
- **Infrastructure:** Google Cloud Platform (GCP) g2‑standard‑24 (2× L4 GPUs)
- **Quantization:** AutoRound (INT4) for final lightweight deployment
- **Evaluation:** L1 (format), L2 (OOD generalization), L3 (extreme OOD / counterfactual)

## 🏆 Google for Startups AI Agents Challenge

This project is submitted to the **Google for Startups AI Agents Challenge (2026)**.

## 📧 Contact

mo.chen@cybernexus.dev