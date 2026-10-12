import numpy as np
import pandas as pd
from typing import Dict, List, Optional
from sklearn.preprocessing import StandardScaler, LabelEncoder

class NetworkFeatureEncoder:
    """Encodes categorical attributes (proto, service, state) and standardizes numerical features."""
    def __init__(self, categorical_columns: Optional[List[str]] = None):
        self.categorical_columns = categorical_columns or ['proto', 'service', 'state']
        self.label_encoders: Dict[str, Dict[str, int]] = {}
        self.scaler = StandardScaler()
        self.feature_names: List[str] = []

    def fit(self, df: pd.DataFrame) -> 'NetworkFeatureEncoder':
        df_encoded = df.copy()
        
        # Learn vocabulary for categorical columns
        for col in self.categorical_columns:
            if col in df_encoded.columns:
                unique_vals = list(df_encoded[col].astype(str).unique())
                # Add unknown token index 0
                val_to_idx = {val: idx + 1 for idx, val in enumerate(unique_vals)}
                val_to_idx['__unknown__'] = 0
                self.label_encoders[col] = val_to_idx
                df_encoded[col] = df_encoded[col].astype(str).map(lambda x: val_to_idx.get(x, 0))

        # Select all numerical columns to scale
        numeric_df = df_encoded.select_dtypes(include=[np.number])
        self.feature_names = list(numeric_df.columns)
        self.scaler.fit(numeric_df)
        return self

    def transform(self, df: pd.DataFrame) -> np.ndarray:
        df_encoded = df.copy()
        for col in self.categorical_columns:
            if col in df_encoded.columns and col in self.label_encoders:
                encoder_map = self.label_encoders[col]
                df_encoded[col] = df_encoded[col].astype(str).map(lambda x: encoder_map.get(x, 0))
                
        # Realign to learned feature names
        for feat in self.feature_names:
            if feat not in df_encoded.columns:
                df_encoded[feat] = 0.0

        numeric_df = df_encoded[self.feature_names]
        return self.scaler.transform(numeric_df)

    def fit_transform(self, df: pd.DataFrame) -> np.ndarray:
        return self.fit(df).transform(df)
