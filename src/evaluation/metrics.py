import numpy as np
from typing import Dict, Any
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score

class ModelEvaluator:
    """Calculates Accuracy, Precision, Recall, F1, FPR, and Confusion Matrix."""
    @staticmethod
    def evaluate(y_true: np.ndarray, y_pred: np.ndarray, probas: np.ndarray = None) -> Dict[str, Any]:
        acc = accuracy_score(y_true, y_pred)
        prec = precision_score(y_true, y_pred, average="weighted", zero_division=0)
        rec = recall_score(y_true, y_pred, average="weighted", zero_division=0)
        f1 = f1_score(y_true, y_pred, average="weighted", zero_division=0)

        # False positive rate computation for binary/multiclass
        cm = confusion_matrix(y_true, y_pred)
        # Approximate FPR from binary/macro CM
        fp = cm.sum(axis=0) - np.diag(cm)
        fn = cm.sum(axis=1) - np.diag(cm)
        tp = np.diag(cm)
        tn = cm.sum() - (fp + fn + tp)
        
        fpr = float(np.mean(fp / (fp + tn + 1e-9)))

        result = {
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4),
            "false_positive_rate": round(fpr, 4),
            "confusion_matrix": cm.tolist()
        }

        if probas is not None and len(np.unique(y_true)) > 1:
            try:
                if probas.shape[1] == 2:
                    auc = roc_auc_score(y_true, probas[:, 1])
                else:
                    auc = roc_auc_score(y_true, probas, multi_class="ovr", average="weighted")
                result["roc_auc"] = round(float(auc), 4)
            except Exception:
                result["roc_auc"] = None

        return result
