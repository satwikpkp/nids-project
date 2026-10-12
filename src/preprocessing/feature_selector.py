import numpy as np
import pandas as pd
from typing import List, Tuple
from sklearn.feature_selection import mutual_info_classif
from sklearn.ensemble import RandomForestClassifier

class IntelligentFeatureSelector:
    """
    Selects top discriminating features (e.g., 15-20 features) using a hybrid combination
    of Mutual Information and Random Forest Gini Feature Importance.
    """
    def __init__(self, target_features: int = 15, random_state: int = 42):
        self.target_features = target_features
        self.random_state = random_state
        self.selected_feature_indices: List[int] = []
        self.selected_feature_names: List[str] = []
        self.feature_importance_scores: dict = {}

    def fit(self, X: np.ndarray, y: np.ndarray, feature_names: List[str]) -> 'IntelligentFeatureSelector':
        n_features = X.shape[1]
        
        # 1. Mutual Information ranking
        mi_scores = mutual_info_classif(X, y, random_state=self.random_state)
        # Normalize to [0, 1]
        mi_norm = (mi_scores - mi_scores.min()) / (mi_scores.max() - mi_scores.min() + 1e-9)

        # 2. Random Forest Importance ranking
        rf = RandomForestClassifier(n_estimators=50, max_depth=10, random_state=self.random_state, n_jobs=-1)
        rf.fit(X, y)
        rf_scores = rf.feature_importances_
        rf_norm = (rf_scores - rf_scores.min()) / (rf_scores.max() - rf_scores.min() + 1e-9)

        # 3. Hybrid Combined Ranking Score
        hybrid_scores = 0.5 * mi_norm + 0.5 * rf_norm
        
        # Select top k indices
        top_k_indices = np.argsort(hybrid_scores)[::-1][:self.target_features]
        self.selected_feature_indices = list(top_k_indices)
        self.selected_feature_names = [feature_names[i] for i in top_k_indices]
        
        for idx in top_k_indices:
            self.feature_importance_scores[feature_names[idx]] = float(hybrid_scores[idx])

        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        if not self.selected_feature_indices:
            return X
        return X[:, self.selected_feature_indices]

    def fit_transform(self, X: np.ndarray, y: np.ndarray, feature_names: List[str]) -> np.ndarray:
        return self.fit(X, y, feature_names).transform(X)
