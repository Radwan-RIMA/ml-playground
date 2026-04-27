import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn.datasets import make_blobs


def load_builtin_dataset(name: str):
    """Load a built-in sklearn or synthetic dataset. Returns (df, target_col, task)."""
    if name == "iris":
        data = datasets.load_iris()
        df = pd.DataFrame(data.data, columns=data.feature_names)
        df["species"] = pd.Categorical.from_codes(data.target, data.target_names)
        return df, "species", "classification"

    elif name == "wine":
        data = datasets.load_wine()
        df = pd.DataFrame(data.data, columns=data.feature_names)
        df["wine_class"] = pd.Categorical.from_codes(data.target, data.target_names)
        return df, "wine_class", "classification"

    elif name == "breast_cancer":
        data = datasets.load_breast_cancer()
        df = pd.DataFrame(data.data, columns=data.feature_names)
        df["diagnosis"] = pd.Categorical.from_codes(data.target, data.target_names)
        return df, "diagnosis", "classification"

    elif name == "digits":
        data = datasets.load_digits()
        df = pd.DataFrame(data.data, columns=[f"pixel_{i}" for i in range(data.data.shape[1])])
        df["digit"] = data.target
        return df, "digit", "classification"

    elif name == "iris_clustering":
        data = datasets.load_iris()
        df = pd.DataFrame(data.data, columns=data.feature_names)
        return df, None, "clustering"

    elif name == "customer_segmentation":
        X, _ = make_blobs(n_samples=200, centers=3, n_features=5, random_state=42)
        df = pd.DataFrame(X, columns=["age", "income", "spending_score", "tenure", "purchase_freq"])
        df["age"] = (df["age"] * 10 + 40).clip(18, 80).round(1)
        df["income"] = (df["income"] * 15000 + 55000).clip(20000, 150000).round(-2)
        df["spending_score"] = (df["spending_score"] * 20 + 50).clip(1, 100).round(1)
        df["tenure"] = (df["tenure"] * 2 + 5).clip(0, 15).round(1)
        df["purchase_freq"] = (df["purchase_freq"] * 5 + 12).clip(1, 30).round(1)
        return df, None, "clustering"

    raise ValueError(f"Unknown dataset: {name}")


DATASET_OPTIONS = {
    "classification": {
        "Iris": "iris",
        "Wine": "wine",
        "Breast Cancer": "breast_cancer",
        "Digits": "digits",
    },
    "clustering": {
        "Iris (Clustering)": "iris_clustering",
        "Customer Segmentation": "customer_segmentation",
    },
}
