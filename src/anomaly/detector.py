import numpy as np
from typing import Tuple

class ZeroDayAnomalyDetector:
    """
    Detects unknown, zero-day, or out-of-distribution attacks that were not in the training set.
    Uses prediction entropy thresholding and max-probability margin bounds.
    """
    def __init__(self, entropy_threshold: float = 1.15, confidence_threshold: float = 0.55):
        self.entropy_threshold = entropy_threshold
        self.confidence_threshold = confidence_threshold

    def evaluate_anomalies(self, ensemble_proba: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Flags samples whose prediction distribution shows high confusion/entropy
        or insufficient confidence as UNKNOWN / ANOMALOUS.
        
        Returns:
            is_anomaly: boolean array of size N
            anomaly_scores: normalized anomaly score in [0, 1]
        """
        # 1. Prediction Entropy
        p = np.clip(ensemble_proba, 1e-12, 1.0)
        entropy = -np.sum(p * np.log(p), axis=1)

        # 2. Maximum probability
        max_prob = np.max(ensemble_proba, axis=1)

        # High entropy OR low max probability indicates unseen zero-day vector
        is_anomaly = (entropy > self.entropy_threshold) | (max_prob < self.confidence_threshold)
        
        # Continuous normalized anomaly score
        # Scale entropy to approx [0, 1]
        norm_entropy = np.clip(entropy / (np.log(ensemble_proba.shape[1]) + 1e-6), 0.0, 1.0)
        norm_uncertainty = 1.0 - max_prob
        anomaly_scores = 0.5 * norm_entropy + 0.5 * norm_uncertainty

        return is_anomaly, anomaly_scores
