# Development & Engineering Rules

This document establishes architectural standards, approved tech libraries, forbidden patterns, error handling conventions, and boundaries for AI agents and human developers contributing to the **Adaptive Lightweight NIDS** codebase.

---

## 1. What to Use (Approved Stack & Conventions)

### 1.1. Machine Learning & Core Data Processing
- **Approved Libraries**:
  - `pandas` (>=2.0.0), `numpy` (>=1.24.0) for high-performance vector operations.
  - `scikit-learn` for preprocessing, metrics, and `RandomForestClassifier`.
  - `xgboost` (>=2.0.0) and `catboost` (>=1.2.0) for gradient boosted trees.
  - `joblib` or `pickle` for model serialization.
  - `psutil` for accurate system memory and CPU cycle profiling.
- **Conventions**:
  - Always separate preprocessing pipelines (encoders, scalers, imputers) from model objects and persist them alongside model weights so inference operates on identical transformations.
  - Fix random seeds (`random_state=42`) across train/test splits, model initializers, and cross-validation folds to guarantee full reproducibility.
  - Vectorize calculations; avoid standard Python `for` loops across large DataFrame rows. Use `.apply()` sparingly and prefer native NumPy/Pandas array operations.

### 1.2. Backend (FastAPI & Async Architecture)
- **Approved Libraries**:
  - `fastapi`, `uvicorn[standard]`
  - `pydantic` (v2) for strict schema definition and request/response validation.
  - `motor` (or `pymongo`) for non-blocking asynchronous MongoDB persistence.
  - `python-jose` for JWT tokens; `passlib[bcrypt]` for cryptographic password hashing.
  - `websockets` for streaming real-time alerts and telemetry.
- **Conventions**:
  - All I/O operations (database queries, network requests, file reading) must use `async`/`await`.
  - Long-running inference on massive batches or background model re-training must be offloaded to background tasks or worker pools to prevent blocking the FastAPI ASGI event loop.
  - Use modular routers (`APIRouter`) partitioned by domain (`/auth`, `/ingest`, `/alerts`, `/telemetry`).

### 1.3. Frontend (React & Modern SOC Dashboard)
- **Approved Libraries**:
  - React 18+ with Vite as the build tool.
  - Tailwind CSS combined with custom CSS design tokens for glassmorphism, glowing badges, and SOC aesthetic.
  - `recharts` or `chart.js` for lightweight responsive visualizations.
  - `lucide-react` for clean, professional cybersecurity iconography.
  - `axios` with interceptors for automatic JWT attachment and refresh handling.
- **Conventions**:
  - Maintain a modular component hierarchy (pages -> composite components -> atomic UI elements).
  - Use centralized React Contexts (`AuthContext`, `TelemetryContext`) for shared cross-application states.
  - Gracefully handle WebSocket reconnects with exponential backoff.

---

## 2. What to Avoid (Forbidden Patterns & Libraries)

### 2.1. Libraries & Dependencies to Avoid
- **DO NOT USE**:
  - Heavy, bloated UI component kits that break dark mode customization or add excessive bundle overhead (avoid Ant Design or legacy Bootstrap).
  - Heavy deep learning frameworks (`TensorFlow` / `Keras`) for the core lightweight tabular tabular classification tasks—keep inference lightweight and fast via tree-based ensembles (`Random Forest`, `XGBoost`, `CatBoost`).
  - Blocking synchronous database drivers (e.g., standard `urllib` or synchronous `pymongo` inside FastAPI async routes without executors).
  - Hardcoded or unpinned global variables in ML inference modules.

### 2.2. Anti-Patterns & Code Smells
- **DO NOT**:
  - Hardcode sensitive credentials (secret keys, database passwords, JWT secrets) directly in code files. Always read from `.env` files using `pydantic-settings` or `python-dotenv`.
  - Leave data leakage in feature engineering (e.g., fitting scalers or encoders on the combined train and test dataset).
  - Write unstructured error messages or silent `except: pass` blocks that swallow runtime exceptions.
  - Train models without tracking memory consumption and inference time overhead.
  - Commit large raw dataset CSVs/PCAPs directly to Git repositories (use `.gitignore` and link data directory locations).

---

## 3. Error Handling & Reliability Standards

### 3.1. Machine Learning Pipelines
- Implement strict schema and dtype validation when receiving input flow records before feeding them into models.
- If a flow contains unseen categorical categories, map them to an `__UNKNOWN__` token or mode imputation rather than raising an unhandled exception.
- If missing values or NaNs are present in streaming data, apply the pipeline's trained imputer or replace with 0/median with logged warnings.

### 3.2. Backend API
- Implement a global FastAPI exception handler returning standardized JSON envelopes:
  ```json
  {
    "success": false,
    "error": {
      "code": "VALIDATION_ERROR",
      "message": "Human readable error details",
      "timestamp": "2026-10-12T12:00:00Z"
    }
  }
  ```
- Protect WebSocket handlers against abrupt client disconnections with proper `try...except WebSocketDisconnect` cleanups.

### 3.3. Frontend Resilience
- Enforce React Error Boundaries around complex data charts to prevent an entire dashboard crash if anomalous data breaks a chart render.
- Render skeleton loaders and empty state indicators during initial data fetches or offline states.

---

## 4. Boundaries for AI Agents & Automated Coders

1. **Architecture Fidelity**:
   - The AI must strictly follow the folder structure specified in `Architecture.md` without inventing unnecessary extraneous directories or altering core module boundaries.
2. **Deterministic Output & Reproducibility**:
   - The AI must configure random seeds across all ML training routines.
3. **No Unprompted Destructive Operations**:
   - Never delete dataset directories, overwrite user database records, or wipe Git commit histories without explicit confirmation.
4. **Clean Code & Self-Documentation**:
   - Every module must include docstrings, type annotations (`typing.Union`, `Optional`, `Dict`, `List`), and clean logging output via `logging` instead of naked `print()` statements.
5. **Memory & Update Rule**:
   - Whenever an AI agent completes a phase, edits an architecture decision, or transitions to a new module, it **must** immediately update `memory.md` to keep the project state transparent.
