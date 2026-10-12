import numpy as np
import pandas as pd
from typing import Tuple, List

class DataCleaner:
    """Handles missing values, inf values, and numeric sanitization for network flow data."""
    def __init__(self):
        self.numeric_medians = {}

    def fit(self, df: pd.DataFrame) -> 'DataCleaner':
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            clean_series = df[col].replace([np.inf, -np.inf], np.nan)
            self.numeric_medians[col] = float(clean_series.median()) if not pd.isna(clean_series.median()) else 0.0
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df_clean = df.copy()
        
        # Replace inf with nan
        df_clean = df_clean.replace([np.inf, -np.inf], np.nan)
        
        # Fill numeric NaNs with learned medians
        for col, median_val in self.numeric_medians.items():
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].fillna(median_val)
                
        # Fill any remaining categorical NaNs with mode or 'unknown'
        cat_cols = df_clean.select_dtypes(include=['object']).columns
        for col in cat_cols:
            df_clean[col] = df_clean[col].fillna('unknown')
            
        return df_clean

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.fit(df).transform(df)
