import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split


def handle_missing_values(df: pd.DataFrame, strategy: str = "mean") -> pd.DataFrame:
    """Fill or drop missing values. strategy: mean/median/mode/drop."""
    df = df.copy()
    if strategy == "drop":
        return df.dropna()
    for col in df.columns:
        if df[col].isnull().any():
            if pd.api.types.is_numeric_dtype(df[col]):
                if strategy == "mean":
                    df[col].fillna(df[col].mean(), inplace=True)
                elif strategy == "median":
                    df[col].fillna(df[col].median(), inplace=True)
                else:
                    df[col].fillna(df[col].mode()[0], inplace=True)
            else:
                df[col].fillna(df[col].mode()[0], inplace=True)
    return df


def encode_categoricals(df: pd.DataFrame, target_col: str, method: str = "label"):
    """Encode categorical feature columns. Returns encoded df."""
    df = df.copy()
    for col in df.columns:
        if col == target_col:
            continue
        if not pd.api.types.is_numeric_dtype(df[col]):
            if method == "onehot":
                dummies = pd.get_dummies(df[col], prefix=col)
                df = pd.concat([df.drop(columns=[col]), dummies], axis=1)
            else:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
    return df


def scale_features(X_train, X_test, method: str = "standard"):
    """Scale feature arrays. Returns (X_train_scaled, X_test_scaled, scaler)."""
    if method == "none":
        return X_train, X_test, None
    scaler = StandardScaler() if method == "standard" else MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, scaler


def prepare_data(df: pd.DataFrame, target_col: str, test_size: float = 0.2,
                 scaling: str = "standard", random_state: int = 42):
    """Full preprocessing pipeline. Returns (X_train, X_test, y_train, y_test, feature_names, scaler)."""
    X = df.drop(columns=[target_col])
    y = df[target_col]
    feature_names = list(X.columns)

    # Encode target if categorical
    if not pd.api.types.is_numeric_dtype(y):
        le = LabelEncoder()
        y = le.fit_transform(y)
    else:
        y = y.values

    X_train, X_test, y_train, y_test = train_test_split(
        X.values, y, test_size=test_size, random_state=random_state, stratify=y if len(np.unique(y)) > 1 else None
    )

    X_train, X_test, scaler = scale_features(X_train, X_test, method=scaling)
    return X_train, X_test, y_train, y_test, feature_names, scaler


def prepare_clustering_data(df: pd.DataFrame, scaling: str = "standard"):
    """Prepare data for clustering (no target). Returns (X_scaled, feature_names, scaler)."""
    feature_names = list(df.columns)
    X = df.values.astype(float)
    if scaling != "none":
        scaler = StandardScaler() if scaling == "standard" else MinMaxScaler()
        X = scaler.fit_transform(X)
    else:
        scaler = None
    return X, feature_names, scaler
