# Google for Startups AI Agents Challenge - Submission Brief

## Project Name
Cyber‑Nexus: Self-Evolving AI Security Agent

## Team
- **Name:** Chen Mo
- **Email:** mo.chen@cybernexus.dev
- **GitHub:** github.com/stardust-ux/defender
- **Organization:** Cyber‑Nexus (Pre‑seed / Bootstrapped)
- **Country:** China

## One‑Sentence Pitch
A self‑evolving autonomous security agent that defends Linux systems against APT attacks, prompt injection, and multi‑turn adversarial threats through continuous red‑team/blue‑team evolution.

## Core Innovation
Unlike traditional rule‑based security tools, Cyber‑Nexus employs a dual‑system cognitive architecture (inspired by Fast‑WAM and LeWM) that combines millisecond‑level intuitive defense with deep sandboxed simulation for complex threat assessment. The system automatically converts every failed defense into training data, enabling weekly self‑iteration without human intervention.

## Technical Highlights
- Fine‑tuned Qwen3‑8B via LoRA (distilled from Qwen3‑30B Teacher)
- Structured `[思考]...[行动] JSON` audit format
- Automated red‑team / blue‑team arena with cognitive auditing
- AST‑level semantic analysis for deobfuscation attacks
- EV‑driven risk assessment for ambiguous instructions

## Demo Plan
- **Model:** Live defense against a series of escalating attacks (from basic prompt injection to multi‑turn APT simulation)
- **Infrastructure:** GCP g2‑standard‑24 instance (2× L4 GPUs)
- **Format:** Web‑based observer dashboard showing real‑time attack/defense verdicts

## Use of Google Cloud
- GPU‑accelerated Teacher distillation (30B model)
- Student model fine‑tuning (8B LoRA)
- Sandboxed RL environment for agent training
- Production deployment via GKE or Cloud Run