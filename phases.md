# Project Implementation Phases

This document defines the roadmap and sequential delivery phases for the **Adaptive Lightweight Network Intrusion Detection System (NIDS)**. It reconciles end-user application delivery milestones (Authentication & Dashboard UI) with the underlying data science, backend, and machine learning pipelines.

---

## High-Level Roadmap Overview

```
+-------------------------------------------------------------------------------------------------+
|                                 APPLICATION MILESTONES                                          |
|                                                                                                 |
|   +---------------------------------------+     +-------------------------------------------+   |
|   |   Phase 1: Authentication & Access    | --> |   Phase 2: SOC Live Monitoring Dashboard  |   |
|   |   (Login, Register, Security, Roles)  |     |   (Real-time Ingest, Alerts, Visuals)     |   |
|   +---------------------------------------+     +-------------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
                                                |
                                                v
+-------------------------------------------------------------------------------------------------+
|                               TECHNICAL & ML PIPELINE PHASES                                    |
|                                                                                                 |
| [P1: Data Ingestion & Baselines]  -->  [P2: Feature Selection]  -->  [P3: Adaptive Ensemble]    |
|                 |                                                                               |
|                 v                                                                               |
| [P4: Unknown Attack Detection]   -->  [P5: FastAPI Backend]    -->  [P6: React Frontend]       |
|                 |                                                                               |
|                 v                                                                               |
| [P7: Resource Profiling & Reports]                                                              |
+-------------------------------------------------------------------------------------------------+
```

---

## Detailed Application & Engineering Phases

### Phase 1: Authentication & Access Control (Login System)
**Goal**: Establish a secure authentication gateway and role-based access control for security operators.

- **Backend Deliverables**:
  - User model with password hashing via `passlib[bcrypt]`.
  - JWT token generation, verification, and refresh routines (`python-jose`).
  - Endpoints:
    - `POST /api/v1/auth/register`
    - `POST /api/v1/auth/login`
    - `GET /api/v1/auth/me`
  - MongoDB user collection schema with role definitions (`admin`, `analyst`, `auditor`).
- **Frontend Deliverables**:
  - High-tech, dark SOC-themed Login screen with animated visual accents.
  - Interactive credential validation and error messaging.
  - Protected route wrappers ensuring unauthenticated users cannot access telemetry feeds.
  - Persistent auth tokens in browser session with automated logout on token expiration.

---

### Phase 2: Real-Time SOC Dashboard & Telemetry Visualizer
**Goal**: Build a mission-critical Security Operations Center (SOC) dashboard displaying network telemetry, live intrusion detections, and model performance.

- **Frontend Core Components**:
  - **Live Traffic Status Panel**: Real-time status badge (`Normal`, `Suspicious`, `Under Attack`) with dynamic color pulses.
  - **Key Metrics KPI Grid**: Total flows analyzed, malicious traffic percentage, average inference latency (ms), and active ensemble accuracy.
  - **Attack Distribution Visualization**: Interactive Donut/Bar charts categorizing threats (DoS, Reconnaissance, Exploits, Generic, Fuzzers, Backdoor).
  - **Live Detections Feed Table**: WebSocket-driven streaming table detailing Timestamp, Source/Destination IPs & Ports, Protocol, Detected Attack Family, Anomaly Tag, and Confidence Score.
  - **System Resource Telemetry Gauge**: Real-time CPU, RAM, and packets-per-second utilization monitors.
- **Backend Service Integration**:
  - WebSocket broadcaster transmitting live flow inferences to connected clients.
  - REST query APIs for filtering alerts by severity, IP range, and timeframe.

---

### Technical Pipeline Phases (AI Builder Instructions)

#### Phase 3: Data Ingestion & Baseline Model Training
- Download/ingest benchmark datasets: **UNSW-NB15** (primary) and **CICIDS2017** (secondary).
- Implement preprocessing pipeline: missing value imputation, categorical encoding (`proto`, `service`, `state`), and scaling (`StandardScaler` / `MinMaxScaler`).
- Train and evaluate baseline individual classifiers:
  - Random Forest
  - XGBoost
  - CatBoost
- Establish benchmark baseline metrics (Accuracy, Precision, Recall, F1, FPR).

#### Phase 4: Feature Selection & Dimension Reduction
- Implement feature selection techniques:
  - Mutual Information (MI)
  - Random Forest Gini Feature Importance
- Filter features from 40+ attributes down to a compact subset of **15–20 features**.
- Benchmark performance curves comparing all features vs. reduced features (quantify accuracy retention vs. computational speedup).

#### Phase 5: Static & Adaptive Ensemble Construction
- **Static Ensemble**: Build baseline soft-voting classifier with fixed model weights.
- **Adaptive Ensemble**: Develop dynamic weight assignment mechanism that adjusts weights per flow/batch based on model confidence, prediction entropy, and historical performance.
- Validate ensemble performance against individual baseline models.

#### Phase 6: Unknown & Zero-Day Attack Detection Module
- Formulate zero-day simulation experiment protocol by deliberately holding out specific attack classes (e.g., omitting *Exploits* or *Fuzzers* from training data).
- Implement anomaly scoring hook using prediction entropy and out-of-distribution confidence estimators.
- Evaluate the rate of correct zero-day flags (`UNKNOWN / ANOMALOUS`) versus false alarms on benign flows.

#### Phase 7: FastAPI Backend Inference Service & Database Integration
- Develop production FastAPI application structure.
- Integrate serialized preprocessor and trained ensemble model pipeline into async inference engine.
- Configure MongoDB collections for storing detection logs, model audit events, and user accounts.
- Implement streaming endpoints for network flow ingestion and WebSocket alert dissemination.

#### Phase 8: Resource Profiling, Ablation Studies & Final Evaluation
- Execute hardware resource profiling scripts:
  - Measure CPU usage (%), peak RAM consumption (MB), model file footprint, single-flow inference latency (ms), and throughput (packets/sec).
- Run automated ablation studies:
  1. Full model vs. without feature selection.
  2. Full adaptive ensemble vs. static ensemble vs. single baseline models.
  3. With vs. without unknown anomaly detection module.
- Generate structured evaluation reports and publication-ready comparative charts.
