import numpy as np
from typing import Dict, Any, List
from src.preprocessing.clean import DataCleaner
from src.preprocessing.encoder import NetworkFeatureEncoder
from src.preprocessing.feature_selector import IntelligentFeatureSelector
from src.models.base_models import BaselineModels
from src.models.static_ensemble import StaticEnsemble
from src.models.adaptive_ensemble import AdaptiveEnsemble
from src.evaluation.metrics import ModelEvaluator
from src.evaluation.profiler import ResourceProfiler

class AblationStudyRunner:
    """
    Executes automated comparative ablation benchmarks:
    1. Full Adaptive Ensemble with 15 Features
    2. Full Model without Feature Selection (All Features)
    3. Static vs Adaptive Ensemble
    4. Individual Single Classifiers (RF only, XGBoost only, CatBoost only)
    """
    def __init__(self, random_state: int = 42):
        self.random_state = random_state

    def run_ablation(
        self,
        X_train_full: np.ndarray,
        y_train: np.ndarray,
        X_test_full: np.ndarray,
        y_test: np.ndarray,
        feature_names: List[str],
        reduced_features: int = 15
    ) -> Dict[str, Any]:
        results = {}

        # 1. Feature selection down to top k
        selector = IntelligentFeatureSelector(target_features=reduced_features, random_state=self.random_state)
        X_train_sel = selector.fit_transform(X_train_full, y_train, feature_names)
        X_test_sel = selector.transform(X_test_full)

        # Baseline Models on selected features
        base_sel = BaselineModels(random_state=self.random_state)
        base_sel.fit(X_train_sel, y_train)

        # Adaptive Ensemble on selected features
        adaptive_sel = AdaptiveEnsemble(base_sel)
        y_pred_adaptive, _, _ = adaptive_sel.predict_proba_with_dynamic_weights(X_test_sel)
        results["adaptive_ensemble_reduced_features"] = {
            **ModelEvaluator.evaluate(y_test, np.argmax(y_pred_adaptive, axis=1), y_pred_adaptive),
            **ResourceProfiler.profile_inference(adaptive_sel, X_test_sel, num_runs=20),
            "feature_count": reduced_features
        }

        # Static Ensemble on selected features
        static_sel = StaticEnsemble(base_sel)
        y_pred_static = static_sel.predict_proba(X_test_sel)
        results["static_ensemble_reduced_features"] = {
            **ModelEvaluator.evaluate(y_test, np.argmax(y_pred_static, axis=1), y_pred_static),
            **ResourceProfiler.profile_inference(static_sel, X_test_sel, num_runs=20),
            "feature_count": reduced_features
        }

        # Single Classifiers (RF only, XGBoost only, CatBoost only)
        rf_preds = base_sel.rf.predict_proba(X_test_sel)
        results["random_forest_only"] = {
            **ModelEvaluator.evaluate(y_test, np.argmax(rf_preds, axis=1), rf_preds),
            **ResourceProfiler.profile_inference(base_sel.rf, X_test_sel, num_runs=20),
            "feature_count": reduced_features
        }

        xgb_preds = base_sel.xgb.predict_proba(X_test_sel)
        results["xgboost_only"] = {
            **ModelEvaluator.evaluate(y_test, np.argmax(xgb_preds, axis=1), xgb_preds),
            **ResourceProfiler.profile_inference(base_sel.xgb, X_test_sel, num_runs=20),
            "feature_count": reduced_features
        }

        cat_preds = base_sel.cat.predict_proba(X_test_sel)
        results["catboost_only"] = {
            **ModelEvaluator.evaluate(y_test, np.argmax(cat_preds, axis=1), cat_preds),
            **ResourceProfiler.profile_inference(base_sel.cat, X_test_sel, num_runs=20),
            "feature_count": reduced_features
        }

        # Full Model without feature selection (all features)
        base_all = BaselineModels(random_state=self.random_state)
        base_all.fit(X_train_full, y_train)
        adaptive_all = AdaptiveEnsemble(base_all)
        y_pred_all, _, _ = adaptive_all.predict_proba_with_dynamic_weights(X_test_full)
        results["adaptive_ensemble_all_features"] = {
            **ModelEvaluator.evaluate(y_test, np.argmax(y_pred_all, axis=1), y_pred_all),
            **ResourceProfiler.profile_inference(adaptive_all, X_test_full, num_runs=20),
            "feature_count": X_train_full.shape[1]
        }

        return results
