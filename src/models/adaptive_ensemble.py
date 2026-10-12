import numpy as np
from typing import Dict, Tuple
from src.models.base_models import BaselineModels

class AdaptiveEnsemble:
    """
    Dynamic weight assignment ensemble.
    Recalibrates weights per-sample or per-batch based on:
    1. Confidence Margin (difference between top 2 class probabilities)
    2. Prediction Entropy (uncertainty measure)
    """
    def __init__(self, base_models: BaselineModels, base_weights: Dict[str, float] = None):
        self.base_models = base_models
        self.base_weights = base_weights or {"rf": 0.33, "xgb": 0.34, "cat": 0.33}

    @staticmethod
    def calculate_entropy(proba: np.ndarray, eps: float = 1e-12) -> np.ndarray:
        # Shannon entropy across probability vector: H = - sum(p * log(p))
        p = np.clip(np.asarray(proba, dtype=np.float64), eps, 1.0)
        return -np.sum(p * np.log(p), axis=1)

    @staticmethod
    def calculate_margin(proba: np.ndarray) -> np.ndarray:
        # Difference between highest and second highest probability
        sorted_p = np.sort(proba, axis=1)
        if sorted_p.shape[1] > 1:
            return sorted_p[:, -1] - sorted_p[:, -2]
        return sorted_p[:, -1]

    def predict_proba_with_dynamic_weights(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Returns:
            ensemble_proba: Final weighted probability distribution
            dynamic_weights: (N, 3) matrix of weights for [rf, xgb, cat] per flow
            uncertainties: (N,) entropy values
        """
        probas = self.base_models.predict_proba_all(X)
        N = X.shape[0]

        # Calculate sample-wise confidence scores for each model
        # Higher margin & lower entropy => higher confidence
        models = ["rf", "xgb", "cat"]
        scores = []
        for m in models:
            p = probas[m]
            margin = self.calculate_margin(p)
            entropy = self.calculate_entropy(p)
            # Confidence score = base_weight * margin / (1 + entropy)
            conf = self.base_weights[m] * (margin + 0.1) / (1.0 + entropy)
            scores.append(conf)

        scores_matrix = np.column_stack(scores) # Shape (N, 3)
        # Normalize across models to sum to 1 per sample
        row_sums = scores_matrix.sum(axis=1, keepdims=True)
        dynamic_weights = scores_matrix / np.maximum(row_sums, 1e-9)

        # Weighted combination
        ensemble_proba = np.zeros_like(probas["rf"])
        for idx, m in enumerate(models):
            w = dynamic_weights[:, idx:idx+1]
            ensemble_proba += w * probas[m]

        # Calculate final ensemble uncertainty
        uncertainties = self.calculate_entropy(ensemble_proba)
        return ensemble_proba, dynamic_weights, uncertainties

    def predict(self, X: np.ndarray) -> np.ndarray:
        ensemble_proba, _, _ = self.predict_proba_with_dynamic_weights(X)
        return np.argmax(ensemble_proba, axis=1)
