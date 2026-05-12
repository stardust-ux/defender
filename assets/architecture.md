# Cyber‑Nexus Architecture Diagrams

## System Overview

```mermaid
graph TD
    A[User Input] --> B[System 1: Fast Defense]
    B -->|Confidence Low| C[System 2: Deep Simulation]
    B -->|Confidence High| D[Execute / Deny]
    C --> E[Sandbox RL Environment]
    E --> F[Expected Value Assessment]
    F --> D
    D --> G[Action Output]
    G --> H[Red-Blue Arena]
    H -->|Failure Case| I[Auto Data Curation]
    I --> J[Incremental Fine‑tuning]
    J --> B