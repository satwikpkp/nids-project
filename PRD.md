# Project Requirements Document (PRD)

## 1. Project Overview
The **Adaptive Lightweight Network Intrusion Detection System (NIDS)** is an advanced, production-ready cybersecurity solution engineered to deliver high-accuracy, real-time threat detection with minimal computational overhead. 

Modern enterprise networks and edge environments (such as IoT gateways and edge servers like Raspberry Pi) face an evolving threat landscape, including high-frequency volumetric attacks, stealthy multi-stage exploits, and novel zero-day vectors. Traditional deep-learning or unoptimized NIDS solutions incur excessive CPU/RAM consumption and latency, making them impractical for resource-constrained network boundaries.

This project addresses these challenges by combining:
- **Intelligent Feature Selection** (filtering high-dimensional flow statistics down to an optimal 15–20 feature subset).
- **Heterogeneous Ensemble Learning** (integrating Random Forest, XGBoost, and CatBoost).
- **Adaptive Dynamic Weighting** (dynamically recalibrating model influence based on inference confidence and performance feedback).
- **Unknown / Zero-Day Anomaly Detection** (flagging unmodeled attack patterns via statistical/confidence anomaly scoring).
- **Microservices & Web Telemetry** (FastAPI backend with streaming telemetry, MongoDB event persistence, and a real-time SOC React dashboard with role-based access).

---

## 2. Targeted Users & Personas

| Persona | Role | Primary Goals & Needs |
| :--- | :--- | :--- |
| **SOC Analysts (L1/L2)** | Security Operations Center | Monitor live network streams, investigate security alerts, review attack classification confidence, and isolate compromised source/destination nodes. |
| **Network & Security Engineers** | Infrastructure & SecOps | Deploy lightweight detection sensors on perimeter firewalls, routers, and edge devices; inspect throughput, packet drop rates, and resource utilization. |
| **Security Researchers / Data Scientists** | Threat Intelligence & ML Ops | Evaluate model drift, analyze zero-day/unknown attack clusters, benchmark feature selection trade-offs, and run offline ablation studies. |
| **System Administrators / IT Managers** | IT Management | Manage user credentials, access controls, audit logs, and overall system health metrics across organization assets. |

---

## 3. Core Features & Functional Requirements

### 3.1. Data Ingestion & Preprocessing
- **Multi-Dataset Support**: Built-in support for standard benchmark datasets (**UNSW-NB15** as primary, **CICIDS2017** as secondary cross-validation).
- **Real-Time & PCAP Capture**: Packet parsing and flow generation via `Scapy`, `Tshark`, and `CICFlowMeter` formats.
- **Robust Preprocessing Pipeline**: Handling missing/infinite values, categorical feature encoding (One-Hot / Target / Label encoding), and robust scaling (`StandardScaler` / `MinMaxScaler`).
- **Feature Selection Engine**: Systematic dimension reduction using Mutual Information and Random Forest Feature Importance to prune 40+ raw network flow features to a lightweight set of **15–20 features** while preserving >99% baseline detection accuracy.

### 3.2. Heterogeneous Ensemble & Adaptive Weighting
- **Baseline Classifiers**: 
  - **Random Forest**: High variance reduction and robustness to noisy tabular attributes.
  - **XGBoost**: Gradient-boosted decision trees optimized for speed and boundary discrimination.
  - **CatBoost**: Superior handling of categorical variations and subtle network feature splits.
- **Static vs. Adaptive Ensemble**:
  - *Static Ensemble*: Soft-voting baseline with fixed weights.
  - *Adaptive Ensemble*: Dynamic real-time weighting adjusting individual model weights per-batch or per-flow using confidence scoring, entropy metrics, and reinforcement/heuristic performance feedback.

### 3.3. Unknown & Zero-Day Attack Detection
- **Zero-Day Holdout Protocol**: Controlled evaluation where specific attack families (e.g., *Exploits*, *Fuzzers*, *Backdoors*) are omitted from the training set.
- **Anomaly Scoring Hook**: Hybrid thresholding on ensemble prediction entropy and out-of-distribution confidence estimators to flag novel threats as `UNKNOWN / ANOMALOUS` instead of misclassifying them as benign traffic.

### 3.4. Evaluation, Resource Profiling & Ablation Studies
- **ML Performance Evaluation**: Automated computation of Accuracy, Precision, Recall, Macro/Micro F1-Score, False Positive Rate (FPR), Confusion Matrix, and ROC-AUC curves.
- **Hardware Resource Profiling**: Continuous telemetry of CPU utilization, RAM footprint, disk I/O, average inference latency per packet/flow (target: sub-millisecond to low milliseconds), and packets processed per second (PPS).
- **Automated Ablation Study Runner**: Scriptable comparative benchmarks comparing:
  1. Full Adaptive Ensemble (reduced features + dynamic weights + anomaly detector).
  2. Full model without feature selection (all 49 features).
  3. Static ensemble vs. single baseline models (RF only, XGBoost only, CatBoost only).
  4. Detection with and without the unknown anomaly detection module.

### 3.5. Backend API & Ingest Service (FastAPI)
- **REST & WebSocket Endpoints**: High-throughput REST API for batch flow ingestion and WebSockets for real-time live telemetry broadcasting to connected clients.
- **Authentication & Authorization**: Secure JWT-based authentication for analysts and administrators.
- **Database Persistence**: MongoDB persistence for detection logs, raw alerts, threat metadata, and historical metric snapshots.

### 3.6. Security Operations Frontend Dashboard (React.js)
- **Secure Authentication**: Dedicated Login/Register screens with session management.
- **Live Traffic Status Panel**: Visual gauge for system state (`Normal Traffic`, `Elevated Risk`, `Under Attack`).
- **Real-Time Feed & Filtering**: Live detection table showing timestamp, source IP/port, destination IP/port, predicted attack family, anomaly flag, and model confidence scores.
- **Statistical Analytics & Charts**: Attack distribution breakdown (DoS, Reconnaissance, Exploits, Generic, etc.), packet throughput time-series, and model confidence trends using Recharts.
- **System Metrics & Telemetry Card**: Live visualization of CPU/RAM load, model inference latency, and active ensemble model weights.

---

## 4. Non-Functional Requirements
- **Performance & Latency**: Flow inference time under 5ms per flow; support for processing thousands of flows/second.
- **Lightweight Footprint**: Base memory footprint operable on constrained hardware (minimum 2 GB RAM, deployable on Raspberry Pi 4 / Docker containers).
- **Reliability & Fault Tolerance**: Resilient exception handling in data parsing; graceful fallback to single models if an ensemble worker times out.
- **Security & Privacy**: Zero plaintext credential storage (Bcrypt hashing), sanitized input payloads, and CORS restriction.
