# Cyber‑Nexus Technical Report

## Abstract

Cyber‑Nexus is a self‑evolving AI security agent that combines a dual‑system cognitive architecture with automated red‑team/blue‑team adversarial training. The system is built on top of fine‑tuned open‑source LLMs and is designed for deployment on resource‑constrained edge hardware (e.g., RTX 5090, L4).

## 1. Introduction

Modern LLM‑based agents face significant security challenges including prompt injection, multi‑turn APT attacks, and reverse engineering. Traditional rule‑based defense mechanisms are inadequate against these evolving threats. Cyber‑Nexus addresses this through continuous evolution driven by adversarial testing feedback.

## 2. System Architecture

### 2.1 Dual‑System Cognitive Framework

| System | Inspired By | Function |
|--------|-------------|----------|
| System 1 | Fast‑WAM | Fast, intuitive defense for routine commands |
| System 2 | LeWM | Deep simulation and deliberation in sandboxed RL environment |

### 2.2 Training Pipeline

1. **Teacher Distillation:** Qwen3‑30B‑A3B generates high‑quality structured training data
2. **Student SFT:** Qwen3‑8B fine‑tuned via LoRA (rank=64)
3. **RL Sandbox:** Model explores defense strategies in a simulated Linux environment
4. **Red‑Blue Arena:** Automated adversarial testing with continuous data feedback

## 3. Key Innovations

- **AST‑level Semantic Analysis:** Defeats code obfuscation attacks
- **EV‑driven Risk Assessment:** Quantitative decision‑making for ambiguous instructions
- **Regression Gate:** Prevents catastrophic forgetting during model evolution
- **Cognitive Audit:** Monitors internal reasoning traces for anomalies

## 4. Evaluation

| Level | Metric | Target |
|-------|--------|--------|
| L1 | Format compliance | > 99% |
| L2 | OOD defense rate | > 90% |
| L3 | Counterfactual defense rate | > 80% |

## 5. Deployment

Final model is quantized to INT4 via AutoRound, reducing size from 16GB to ~5GB, enabling deployment on a single RTX 5090 or L4 GPU.

## References

See `docs/full_report.md` for detailed technical references and literature review.