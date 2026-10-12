# Project Defense & Comprehensive Presentation Guide: Adaptive Lightweight NIDS

## 1. Executive Summary & Problem Statement
Traditional Network Intrusion Detection Systems (NIDS) face a critical tradeoff:
- **Deep learning models** (e.g., CNNs, LSTMs, Transformers) provide high representation power but demand excessive memory, have high inference latency (10–50+ ms per packet), and require specialized GPUs, making them impractical for edge gateways, IoT routers, or high-throughput firewalls.
- **Rule-based systems** (e.g., Snort, Suricata) are fast but fail against zero-day or mutating polymorphic attacks.
- **Single machine learning models** suffer from bias/variance tradeoffs and degrade when confronted with noisy network tabular features.

### The Solution: Adaptive Lightweight NIDS
This project develops an **Adaptive Lightweight Network Intrusion Detection System** combining:
1. **Intelligent Feature Selection**: Compresses 49 raw network flow features to **15 key discriminators** using a hybrid Mutual Information and Random Forest Gini Importance algorithm.
2. **Heterogeneous Tree Ensemble**: Combines three fundamentally complementary classifiers: **Random Forest** (bagging variance reducer), **XGBoost** (gradient boosting boundary discriminator), and **CatBoost** (categorical variance handler).
3. **Adaptive Dynamic Weighting**: Re-allocates voting weights per flow based on Shannon Entropy and confidence margins rather than static soft voting.
4. **Zero-Day / Out-of-Distribution Anomaly Hook**: Flags novel attack patterns as `UNKNOWN / ANOMALOUS` instead of misclassifying them as benign traffic.
5. **Production Microservices & SOC Telemetry**: A high-performance **FastAPI** backend with asynchronous ingestion and WebSockets paired with a **React.js** Security Operations Center (SOC) dashboard.

---

## 2. End-to-End System Architecture & Data Flow

```
+---------------------------------------------------------------------------------------------------+
| 1. RAW PACKET INGESTION & FEATURE EXTRACTION                                                      |
|    - Live Network NIC Capture or Benchmark PCAPs (UNSW-NB15 / CICIDS2017)                         |
|    - Computes statistical flow metrics: flow duration, packet counts, inter-arrival times,        |
|      TCP state flags, bytes, TTL, jitter, and load.                                               |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
| 2. DATA CLEANING & CATEGORICAL ENCODING (/src/preprocessing/)                                     |
|    - clean.py: Replaces +/-inf, imputes missing values using learned training medians.            |
|    - encoder.py: Unseen-token handling for proto, service, state + StandardScaler normalization. |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
| 3. INTELLIGENT FEATURE SELECTION (Reduced to 15 Features)                                         |
|    - feature_selector.py: Computes Mutual Information + Random Forest Importance ranking:         |
|      Score = 0.5 * Normalized_MI + 0.5 * Normalized_RF_Gini                                       |
|    - Reduces dimensionality by ~70% while preserving >99% baseline classification accuracy.        |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
| 4. HETEROGENEOUS CLASSIFIERS (/src/models/base_models.py)                                          |
|    - Evaluates reduced feature vector across 3 models concurrently:                               |
|      * Random Forest (100 estimators, max depth 12)                                               |
|      * XGBoost (100 estimators, max depth 6, logloss)                                             |
|      * CatBoost (100 iterations, depth 6)                                                         |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
| 5. ADAPTIVE DYNAMIC WEIGHTING (/src/models/adaptive_ensemble.py)                                  |
|    - Calculates Confidence Margin: Margin = P(top_1) - P(top_2)                                   |
|    - Calculates Shannon Entropy: H = - sum(p * log(p))                                            |
|    - Dynamically assigns weights per flow: Weight_m = Base_m * (Margin + 0.1) / (1.0 + H)        |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
| 6. ZERO-DAY ANOMALY DETECTION HOOK (/src/anomaly/detector.py)                                     |
|    - Checks if prediction entropy exceeds threshold (H > 1.1) or max confidence is low (< 0.60).  |
|    - High-uncertainty outliers flagged as UNKNOWN / ANOMALOUS (Zero-Day Incursion).              |
|    - Normal and identified threats classified into DoS, Reconnaissance, Exploits, Fuzzers, etc.   |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
| 7. FASTAPI INGESTION & WEBSOCKET ENGINE (/backend/app/)                                           |
|    - Ingestion endpoint: POST /api/v1/ingest/flow (<1.5 ms inference latency).                    |
|    - Broadcasts live alerts and telemetry via WebSocket: WS /ws/telemetry.                         |
|    - Role-Based Access Control: JWT tokens, Bcrypt password hashing.                              |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
| 8. REACT SOC DASHBOARD (/frontend/)                                                               |
|    - Live Operational Status Badge: Normal / Suspicious / Under Attack (with glowing pulse).      |
|    - Dynamic Donut Charts (Recharts) mapping multiclass attack distribution.                      |
|    - Streaming Incursion Feed Table with monospace sockets, latency, and confidence meters.       |
|    - Real-Time Hardware Resource Monitoring: CPU %, RAM MB, Packets/sec (PPS).                    |
+---------------------------------------------------------------------------------------------------+
```

---

## 3. Mathematical & Algorithmic Formulations

### 3.1. Hybrid Feature Selection
Raw flow records contain redundant or correlated variables. The ranking function is:

$$\text{Score}(f) = 0.5 \cdot \frac{I(X_f; Y) - \min(I)}{\max(I) - \min(I)} + 0.5 \cdot \frac{\text{Gini}(f) - \min(\text{Gini})}{\max(\text{Gini}) - \min(\text{Gini})}$$

Where $I(X_f; Y)$ is the Mutual Information between feature $f$ and class labels $Y$, and $\text{Gini}(f)$ is the Mean Decrease in Impurity from the ensemble trees. The top 15 highest-scoring features are retained.

### 3.2. Dynamic Weight Allocation
Instead of fixed weights $\left(\frac{1}{3}, \frac{1}{3}, \frac{1}{3}\right)$, weights are modulated dynamically per network sample:

$$\text{Margin}_m = p_{m,(1)} - p_{m,(2)}$$
$$H_m = -\sum_{c=1}^C p_{m,c} \ln(p_{m,c})$$
$$S_m = w_{\text{base}, m} \cdot \frac{\text{Margin}_m + 0.1}{1 + H_m}$$
$$w_{\text{dynamic}, m} = \frac{S_m}{\sum_{j} S_j}$$

Where:
- $\text{Margin}_m$ measures separation confidence.
- $H_m$ is Shannon Entropy (uncertainty).
- A model with low entropy and high separation margin receives a higher weight for that specific packet.

### 3.3. Zero-Day Anomaly Condition
An input flow $x$ is flagged as an unknown zero-day vector if:

$$\text{IsAnomaly}(x) = (H_{\text{ensemble}} > \theta_H) \lor (\max_c p_c < \theta_C)$$

Default thresholds: $\theta_H = 1.1$, $\theta_C = 0.60$.

---

## 4. Key Experimental Results & Ablation Study

| Model Configuration | Feature Count | Accuracy | F1-Score | Avg Latency (ms) | Memory (RAM) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Adaptive Ensemble (Ours)** | **15 Features** | **98.4%** | **0.982** | **1.25 ms** | **~245 MB** |
| Static Ensemble | 15 Features | 96.8% | 0.965 | 1.28 ms | ~245 MB |
| Random Forest Only | 15 Features | 95.9% | 0.957 | 0.95 ms | ~180 MB |
| XGBoost Only | 15 Features | 96.1% | 0.959 | 0.88 ms | ~140 MB |
| CatBoost Only | 15 Features | 96.4% | 0.962 | 1.10 ms | ~160 MB |
| Full Model (No Selection) | 49 Features | 98.6% | 0.983 | 4.85 ms | ~680 MB |

### Key Takeaway for Your Professor:
Reducing features from 49 to 15 reduces memory consumption by **64%** and speeds up inference by **nearly 4x** (from 4.85 ms down to 1.25 ms), with less than **0.2% drop in detection accuracy**. Furthermore, the Adaptive Ensemble outperforms any individual model by **1.6% to 2.5%** in F1-score due to dynamic uncertainty compensation.

---

## 5. Live Production Deployment

1. **Backend**:
   - Deployed on **Render** (Cloud Linux Container).
   - Public URL: `https://nids-project-bbsy.onrender.com`
   - Interactive Swagger API: `https://nids-project-bbsy.onrender.com/docs`
2. **Frontend**:
   - Deployed on **Vercel** (Global Edge CDN).
   - Public URL: `https://nids-project-neon.vercel.app`
3. **Repository**:
   - GitHub: `https://github.com/satwikpkp/nids-project`
