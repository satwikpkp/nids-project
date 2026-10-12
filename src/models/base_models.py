import numpy as np
from typing import Dict, Any, Tuple
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier

class BaselineModels:
    """Encapsulates the 3 heterogeneous baseline classifiers: Random Forest, XGBoost, and CatBoost."""
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.rf = RandomForestClassifier(
            n_estimators=100,
            max_depth=12,
            random_state=random_state,
            n_jobs=-1
        )
        self.xgb = XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            eval_metric="logloss",
            random_state=random_state,
            n_jobs=-1
        )
        self.cat = CatBoostClassifier(
            iterations=100,
            depth=6,
            learning_rate=0.1,
            verbose=0,
            random_seed=random_state
        )
        self.is_fitted = False

    def fit(self, X_train: np.ndarray, y_train: np.ndarray):
        self.rf.fit(X_train, y_train)
        self.xgb.fit(X_train, y_train)
        self.cat.fit(X_train, y_train)
        self.is_fitted = True
        return self

    def predict_proba_all(self, X: np.ndarray) -> Dict[str, np.ndarray]:
        if not self.is_fitted:
            raise RuntimeError("Models must be fitted before predict_proba_all can be called.")
        return {
            "rf": self.rf.predict_proba(X),
            "xgb": self.xgb.predict_proba(X),
            "cat": self.cat.predict_proba(X)
        }
