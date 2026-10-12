import numpy as np
from typing import Dict, Optional
from src.models.base_models import BaselineModels

class StaticEnsemble:
    """Fixed-weight soft-voting ensemble combining RF, XGBoost, and CatBoost."""
    def __init__(self, base_models: BaselineModels, weights: Optional[Dict[str, float]] = None):
        self.base_models = base_models
        # Default balanced soft weights
        self.weights = weights or {"rf": 0.333, "xgb": 0.334, "cat": 0.333}

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        probas = self.base_models.predict_proba_all(X)
        w_rf = self.weights["rf"]
        w_xgb = self.weights["xgb"]
        w_cat = self.weights["cat"]
        total_w = w_rf + w_xgb + w_cat

        ensemble_proba = (
            w_rf * probas["rf"] +
            w_xgb * probas["xgb"] +
            w_cat * probas["cat"]
        ) / total_w
        return ensemble_proba

    def predict(self, X: np.ndarray) -> np.ndarray:
        return np.argmax(self.predict_proba(X), axis=1)
