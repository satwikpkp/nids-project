import numpy as np
import pandas as pd
import pytest
from src.preprocessing.clean import DataCleaner
from src.preprocessing.encoder import NetworkFeatureEncoder
from src.preprocessing.feature_selector import IntelligentFeatureSelector
from src.models.base_models import BaselineModels
from src.models.static_ensemble import StaticEnsemble
from src.models.adaptive_ensemble import AdaptiveEnsemble
from src.anomaly.detector import ZeroDayAnomalyDetector
from src.anomaly.zero_day_eval import ZeroDayHoldoutProtocol
from src.evaluation.metrics import ModelEvaluator
from src.evaluation.profiler import ResourceProfiler
from src.evaluation.ablation import AblationStudyRunner

def generate_mock_traffic(n_samples=200):
    np.random.seed(42)
    data = {
        "dur": np.random.exponential(1.5, n_samples),
        "proto": np.random.choice(["tcp", "udp", "icmp"], n_samples),
        "service": np.random.choice(["http", "dns", "ssh", "ftp", "-"], n_samples),
        "state": np.random.choice(["FIN", "INT", "CON", "REQ"], n_samples),
        "spkts": np.random.randint(1, 100, n_samples),
        "dpkts": np.random.randint(0, 100, n_samples),
        "sbytes": np.random.randint(40, 10000, n_samples),
        "dbytes": np.random.randint(0, 10000, n_samples),
        "rate": np.random.uniform(0.1, 50.0, n_samples),
        "sttl": np.random.randint(30, 255, n_samples),
        "dttl": np.random.randint(30, 255, n_samples),
        "sload": np.random.uniform(100.0, 50000.0, n_samples),
        "dload": np.random.uniform(0.0, 50000.0, n_samples),
        "sloss": np.random.randint(0, 10, n_samples),
        "dloss": np.random.randint(0, 10, n_samples),
        "sinpkt": np.random.uniform(0.01, 100.0, n_samples),
        "dinpkt": np.random.uniform(0.01, 100.0, n_samples),
        "sjit": np.random.uniform(0.0, 1000.0, n_samples),
        "djit": np.random.uniform(0.0, 1000.0, n_samples),
        "attack_cat": np.random.choice(["Normal", "DoS", "Exploits", "Fuzzers"], n_samples, p=[0.7, 0.1, 0.1, 0.1])
    }
    # Introduce some infs and nans to test cleaning
    data["dur"][0] = np.nan
    data["rate"][1] = np.inf
    df = pd.DataFrame(data)
    y = (df["attack_cat"] != "Normal").astype(int).values
    return df, y

def test_preprocessing_pipeline():
    df, y = generate_mock_traffic()
    cleaner = DataCleaner()
    df_clean = cleaner.fit_transform(df)
    assert not np.isnan(df_clean["dur"].iloc[0])
    assert not np.isinf(df_clean["rate"].iloc[1])

    feature_cols = [c for c in df_clean.columns if c != "attack_cat"]
    encoder = NetworkFeatureEncoder()
    X = encoder.fit_transform(df_clean[feature_cols])
    assert X.shape[0] == len(df)
    assert X.shape[1] > 10

    # Feature selection down to 10
    selector = IntelligentFeatureSelector(target_features=10)
    X_sel = selector.fit_transform(X, y, encoder.feature_names)
    assert X_sel.shape[1] == 10
    assert len(selector.selected_feature_names) == 10

def test_models_and_ensembles():
    df, y = generate_mock_traffic()
    cleaner = DataCleaner()
    df_clean = cleaner.fit_transform(df)
    feature_cols = [c for c in df_clean.columns if c != "attack_cat"]
    encoder = NetworkFeatureEncoder()
    X = encoder.fit_transform(df_clean[feature_cols])
    selector = IntelligentFeatureSelector(target_features=8)
    X_sel = selector.fit_transform(X, y, encoder.feature_names)

    # Fit baselines
    base = BaselineModels()
    base.fit(X_sel, y)

    # Static Ensemble
    static_ens = StaticEnsemble(base)
    probas_static = static_ens.predict_proba(X_sel)
    preds_static = static_ens.predict(X_sel)
    assert probas_static.shape == (len(df), 2)
    assert len(preds_static) == len(df)

    # Adaptive Ensemble
    adaptive_ens = AdaptiveEnsemble(base)
    probas_adapt, dyn_weights, uncertainties = adaptive_ens.predict_proba_with_dynamic_weights(X_sel)
    assert probas_adapt.shape == (len(df), 2)
    assert dyn_weights.shape == (len(df), 3) # weights for rf, xgb, cat
    assert np.allclose(dyn_weights.sum(axis=1), 1.0) # sum to 1
    assert len(uncertainties) == len(df)

def test_anomaly_and_zero_day():
    df, _ = generate_mock_traffic()
    holdout = ZeroDayHoldoutProtocol(holdout_classes=["Exploits", "Fuzzers"])
    train_seen, zero_day = holdout.split_dataset(df)
    assert not any(train_seen["attack_cat"].isin(["Exploits", "Fuzzers"]))
    assert all(zero_day["attack_cat"].isin(["Exploits", "Fuzzers"]))

    # Anomaly detector
    detector = ZeroDayAnomalyDetector(entropy_threshold=0.6, confidence_threshold=0.6)
    mock_confused_probas = np.array([[0.51, 0.49], [0.99, 0.01]])
    is_ano, ano_scores = detector.evaluate_anomalies(mock_confused_probas)
    assert is_ano[0] == True # High confusion sample flagged as anomaly
    assert is_ano[1] == False # High confidence benign sample not flagged

def test_evaluation_and_profiler():
    y_true = np.array([0, 0, 1, 1, 0])
    y_pred = np.array([0, 0, 1, 0, 0])
    probas = np.array([[0.9, 0.1], [0.8, 0.2], [0.1, 0.9], [0.6, 0.4], [0.95, 0.05]])
    metrics = ModelEvaluator.evaluate(y_true, y_pred, probas)
    assert "accuracy" in metrics
    assert "precision" in metrics
    assert "f1_score" in metrics
    assert "false_positive_rate" in metrics

def test_ablation_runner():
    df, y = generate_mock_traffic(n_samples=150)
    cleaner = DataCleaner()
    df_clean = cleaner.fit_transform(df)
    feature_cols = [c for c in df_clean.columns if c != "attack_cat"]
    encoder = NetworkFeatureEncoder()
    X = encoder.fit_transform(df_clean[feature_cols])

    X_train, X_test = X[:100], X[100:]
    y_train, y_test = y[:100], y[100:]

    runner = AblationStudyRunner()
    results = runner.run_ablation(X_train, y_train, X_test, y_test, encoder.feature_names, reduced_features=8)
    assert "adaptive_ensemble_reduced_features" in results
    assert "static_ensemble_reduced_features" in results
    assert "random_forest_only" in results
    assert "adaptive_ensemble_all_features" in results
    assert results["adaptive_ensemble_reduced_features"]["feature_count"] == 8
