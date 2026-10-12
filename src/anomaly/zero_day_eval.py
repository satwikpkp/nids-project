import numpy as np
import pandas as pd
from typing import Dict, List, Tuple

class ZeroDayHoldoutProtocol:
    """
    Simulates zero-day attacks by systematically holding out specific attack classes
    (e.g., Exploits, Fuzzers, or Backdoors) during training, then measuring detection
    rates when evaluated on the holdout classes.
    """
    def __init__(self, holdout_classes: List[str]):
        self.holdout_classes = holdout_classes

    def split_dataset(
        self,
        df: pd.DataFrame,
        attack_col: str = "attack_cat"
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Splits data into:
        1. Training candidate set: Contains normal traffic and seen attack classes only.
        2. Zero-day evaluation set: Contains held-out unseen attack classes.
        """
        is_holdout = df[attack_col].isin(self.holdout_classes)
        train_seen_df = df[~is_holdout].copy()
        zero_day_df = df[is_holdout].copy()
        return train_seen_df, zero_day_df
