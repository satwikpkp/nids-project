# System Architecture & Technical Design

## 1. High-Level System Architecture & Flow

The system processes incoming raw network traffic or pre-captured flow logs through a multi-stage machine learning and microservice pipeline, surfacing results to security operators in real-time.

```
                           +---------------------------+
                           | Network Traffic / PCAP   |
                           +---------------------------+
                                         |
                                         v
                           +---------------------------+
                           |    Feature Extraction     |
                           |     (CICFlowMeter/Scapy)  |
                           +---------------------------+
                                         |
                                         v
                           +---------------------------+
                           |     Data Preprocessing    |
                           |  (Cleaning, Scaling, Enc) |
                           +---------------------------+
                                         |
                                         v
                           +---------------------------+
                           |     Feature Selection     |
                           |  (Mutual Info / RF Imp)   |
                           +---------------------------+
                                         |
                                         v
                           +---------------------------+
                           |  Reduced Feature Set (15) |
                           +---------------------------+
                                         |
                 +-----------------------+-----------------------+
                 |                       |                       |
                 v                       v                       v
         +---------------+       +---------------+       +---------------+
         | Random Forest |       |    XGBoost    |       |   CatBoost    |
         +---------------+       +---------------+       +---------------+
                 |                       |                       |
                 +-----------------------+-----------------------+
                                         |
                                         v
                           +---------------------------+
                           |     Adaptive Ensemble     |
                           |     (Dynamic Weighting)   |
                           +---------------------------+
                                         |
                       +-----------------+-----------------+
                       |                                   |
                       v                                   v
             +--------------------+              +--------------------+
             | Known Attack Class |              |  Unknown / Anomaly |
             | (DoS, Exploit, etc)|              |  Detection Engine  |
             +--------------------+              +--------------------+
                       |                                   |
                       +-----------------+-----------------+
                                         |
                                         v
                           +---------------------------+
                           |  FastAPI Backend Service  |
                           |  - REST Ingestion API     |
                           |  - WebSocket Telemetry    |
                           |  - Auth & Alert Manager   |
                           +---------------------------+
                             |                       |
                             v                       v
               +--------------------+         +--------------------+
               |  MongoDB Database  |         | React.js Dashboard |
               | (Alerts & Metrics) |         | (Real-time Web UI) |
               +--------------------+         +--------------------+
```

---

## 2. Component Pipeline Breakdown

1. **Feature Extraction Layer**:
   - Ingests raw network PCAPs or live NIC packet flows via Scapy / Tshark / CICFlowMeter.
   - Computes statistical flow attributes: flow duration, packet counts, inter-arrival times, TCP flags, header lengths, byte ratios.

2. **Preprocessing & Feature Selection Layer (`/src/preprocessing/`)**:
   - Implements automated imputation for missing/inf values.
   - Applies categorical encoding (`service`, `proto`, `state`) and standardizes features via `StandardScaler` / `MinMaxScaler`.
   - Feature selector applies a hybrid Mutual Information + Tree Gini Importance filter to distill 40+ raw features down to 15–20 high-value discriminating attributes.

3. **Inference & Adaptive Ensemble Layer (`/src/models/`, `/src/anomaly/`)**:
   - Baseline models: Random Forest, XGBoost, and CatBoost evaluate the reduced vector in parallel.
   - Dynamic weight assigner recalibrates weights according to prediction entropy, margin confidence, and recent validation accuracy.
   - Unknown attack detector evaluates prediction distribution divergence; low-confidence outliers are redirected and classified as `UNKNOWN / ANOMALOUS`.

4. **API & Data Persistence Service (`/backend/`)**:
   - FastAPI orchestrates flow ingestion, asynchronous prediction pipelines, and telemetry emission.
   - In-memory event bus or WebSocket broadcast pushes real-time alert updates to connected SOC clients.
   - MongoDB stores immutable detection events, user accounts, and aggregated time-series metrics.

5. **Client Presentation Layer (`/frontend/`)**:
   - Single Page Application (SPA) built with React.js, Tailwind CSS, and Recharts.
   - Features protected routes, authentication guards, live incident timelines, and interactive telemetry charts.

---

## 3. Technology Stack

### 3.1. Core Machine Learning & Data Processing
- **Language**: Python 3.10+
- **Data Manipulation**: `pandas`, `numpy`
- **Machine Learning**: `scikit-learn`, `xgboost`, `catboost`
- **Deep Learning / RL (Optional/PPO)**: `torch`
- **Visualization & Profiling**: `matplotlib`, `seaborn`, `psutil`
- **Packet & Flow Processing**: `scapy`, `tshark`, `cicflowmeter`

### 3.2. Backend & Database
- **Web Framework**: `FastAPI`
- **ASGI Server**: `uvicorn`
- **Database**: `MongoDB` (using `motor` for async I/O or `pymongo`)
- **Authentication**: `python-jose` (JWT), `passlib` (Bcrypt password hashing)
- **Validation & Serialization**: `pydantic` (v2)

### 3.3. Frontend Dashboard
- **Framework**: React.js (Vite)
- **Styling**: Tailwind CSS, Vanilla CSS custom design tokens
- **Data Visualization**: `recharts` / `chart.js`
- **Icons**: `lucide-react`
- **HTTP & Sockets**: `axios`, native WebSocket API

### 3.4. DevOps & Deployment
- **Containerization**: Docker, Docker Compose
- **Target Environments**: Linux/Windows Workstations, Dockerized Microservices, Edge Hardware (Raspberry Pi 4)

---

## 4. Folder & File Structure

```
nids-project/
├── data/
│   ├── raw/                       # Original UNSW-NB15 / CICIDS2017 CSV and PCAP files
│   └── processed/                 # Cleaned, normalized, and feature-selected datasets
├── notebooks/                     # Exploratory data analysis, feature correlation & prototyping
├── src/
│   ├── preprocessing/             # Data cleaning, categorical encoding, scaling & feature selection
│   │   ├── __init__.py
│   │   ├── clean.py               # Data sanitization, missing value handling
│   │   ├── encoder.py             # One-hot/label encoders with pipeline persistence
│   │   └── feature_selector.py    # Mutual information and RF feature ranking
│   ├── models/                    # Base ML classifiers and ensemble strategies
│   │   ├── __init__.py
│   │   ├── base_models.py         # RF, XGBoost, CatBoost wrappers and training routines
│   │   ├── static_ensemble.py     # Fixed weighted soft-voting ensemble
│   │   └── adaptive_ensemble.py   # Dynamic weight adjustment and entropy scoring
│   ├── anomaly/                   # Unknown and zero-day threat detection logic
│   │   ├── __init__.py
│   │   ├── zero_day_eval.py       # Attack-class holdout protocol
│   │   └── detector.py            # Anomaly scoring and out-of-distribution thresholding
│   └── evaluation/                # Performance assessment, resource profiling & ablation
│       ├── __init__.py
│       ├── metrics.py             # Accuracy, precision, recall, F1, FPR, ROC-AUC
│       ├── profiler.py            # CPU, RAM, latency (ms), and packets/sec benchmark
│       └── ablation.py            # Automated ablation study test runner
├── backend/                       # FastAPI application service
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                # FastAPI app initialization, routes & WebSocket handler
│   │   ├── config.py              # Environment settings, secret keys, DB URIs
│   │   ├── database.py            # MongoDB connection manager
│   │   ├── models/                # Pydantic data schemas & DB document models
│   │   │   ├── user.py
│   │   │   ├── packet.py
│   │   │   └── alert.py
│   │   ├── routes/                # Endpoint controllers
│   │   │   ├── auth.py            # Login, register, token refresh
│   │   │   ├── ingest.py          # Real-time packet/flow ingestion & batch prediction
│   │   │   ├── alerts.py          # Alert history, querying & filtering
│   │   │   └── telemetry.py       # System resource & model health metrics
│   │   └── services/              # Inference engine, background tasks & socket broadcaster
│   │       ├── inference.py
│   │       └── socket_manager.py
├── frontend/                      # React.js web dashboard
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/            # Reusable UI components (Cards, Tables, Badges, Charts)
│   │   │   ├── Navbar.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── TrafficStatusBadge.jsx
│   │   │   ├── DetectionFeedTable.jsx
│   │   │   ├── MetricsCard.jsx
│   │   │   └── AttackDistributionChart.jsx
│   │   ├── context/               # Global state (AuthContext, SocketContext)
│   │   │   ├── AuthContext.jsx
│   │   │   └── TelemetryContext.jsx
│   │   ├── pages/                 # Primary page views
│   │   │   ├── Login.jsx          # User authentication page
│   │   │   ├── Register.jsx       # User registration page
│   │   │   ├── Dashboard.jsx      # Main live SOC dashboard
│   │   │   ├── Analytics.jsx      # Historical reports & ablation views
│   │   │   └── Settings.jsx       # Detection thresholds & model parameters
│   │   ├── services/              # API and WebSocket client abstractions
│   │   │   ├── api.js
│   │   │   └── socket.js
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── tests/                         # Unit and integration test suites
│   ├── test_preprocessing.py
│   ├── test_models.py
│   ├── test_anomaly.py
│   └── test_api.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```
