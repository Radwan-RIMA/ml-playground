import pandas as pd
from typing import Tuple, List


def validate_uploaded_csv(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """Return (is_valid, list_of_errors)."""
    errors = []

    if len(df) < 50:
        errors.append(f"Dataset has only {len(df)} rows. Minimum required: 50.")

    feature_cols = [c for c in df.columns]
    if len(feature_cols) < 3:
        errors.append("Dataset must have at least 2 feature columns plus a target column.")

    if len(df.columns) > 100:
        errors.append(f"Dataset has {len(df.columns)} columns. Maximum allowed: 100.")

    all_same = all(df[c].nunique() == 1 for c in df.columns)
    if all_same:
        errors.append("All columns have constant values — no useful features found.")

    return len(errors) == 0, errors


def detect_column_types(df: pd.DataFrame):
    """Return dict of {col: 'numeric'|'categorical'} and missing value counts."""
    col_types = {}
    missing_counts = {}
    for col in df.columns:
        missing_counts[col] = df[col].isnull().sum()
        if pd.api.types.is_numeric_dtype(df[col]):
            col_types[col] = "numeric"
        else:
            col_types[col] = "categorical"
    return col_types, missing_counts
