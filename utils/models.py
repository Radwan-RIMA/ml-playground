import time
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.cluster import KMeans


MODEL_REGISTRY = {
    "KNN": {
        "name": "K-Nearest Neighbors",
        "task": "classification",
        "params": {
            "n_neighbors": {"type": "slider", "min": 1, "max": 20, "default": 5, "step": 1},
            "weights": {"type": "select", "options": ["uniform", "distance"], "default": "uniform"},
            "metric": {"type": "select", "options": ["euclidean", "manhattan"], "default": "euclidean"},
        },
        "best_for": "Small datasets",
    },
    "Logistic Regression": {
        "name": "Logistic Regression",
        "task": "classification",
        "params": {
            "C": {"type": "slider", "min": 0.01, "max": 10.0, "default": 1.0, "step": 0.01},
            "max_iter": {"type": "slider", "min": 100, "max": 1000, "default": 100, "step": 50},
            "solver": {"type": "select", "options": ["lbfgs", "liblinear"], "default": "lbfgs"},
        },
        "best_for": "Linear boundaries",
    },
    "Decision Tree": {
        "name": "Decision Tree",
        "task": "classification",
        "params": {
            "max_depth": {"type": "slider", "min": 1, "max": 20, "default": 5, "step": 1},
            "min_samples_split": {"type": "slider", "min": 2, "max": 10, "default": 2, "step": 1},
            "criterion": {"type": "select", "options": ["gini", "entropy"], "default": "gini"},
        },
        "best_for": "Explainability",
    },
    "Random Forest": {
        "name": "Random Forest",
        "task": "classification",
        "params": {
            "n_estimators": {"type": "slider", "min": 10, "max": 200, "default": 100, "step": 10},
            "max_depth": {"type": "slider", "min": 1, "max": 20, "default": 10, "step": 1},
            "min_samples_split": {"type": "slider", "min": 2, "max": 10, "default": 2, "step": 1},
        },
        "best_for": "Best accuracy",
    },
    "SVM": {
        "name": "Support Vector Machine",
        "task": "classification",
        "params": {
            "C": {"type": "slider", "min": 0.1, "max": 10.0, "default": 1.0, "step": 0.1},
            "kernel": {"type": "select", "options": ["linear", "rbf", "poly"], "default": "rbf"},
            "gamma": {"type": "select", "options": ["scale", "auto"], "default": "scale"},
        },
        "best_for": "High-dimensional data",
    },
    "K-Means": {
        "name": "K-Means Clustering",
        "task": "clustering",
        "params": {
            "n_clusters": {"type": "slider", "min": 2, "max": 10, "default": 3, "step": 1},
            "max_iter": {"type": "slider", "min": 100, "max": 500, "default": 300, "step": 50},
            "init": {"type": "select", "options": ["k-means++", "random"], "default": "k-means++"},
        },
        "best_for": "Finding natural groups",
    },
}


def build_model(model_name: str, params: dict):
    """Instantiate a model from name and hyperparams dict."""
    if model_name == "KNN":
        return KNeighborsClassifier(**params)
    elif model_name == "Logistic Regression":
        return LogisticRegression(random_state=42, **params)
    elif model_name == "Decision Tree":
        return DecisionTreeClassifier(random_state=42, **params)
    elif model_name == "Random Forest":
        return RandomForestClassifier(random_state=42, n_jobs=-1, **params)
    elif model_name == "SVM":
        return SVC(random_state=42, probability=True, **params)
    elif model_name == "K-Means":
        return KMeans(random_state=42, **params)
    raise ValueError(f"Unknown model: {model_name}")


def train_model(model, X_train, y_train):
    """Fit model and return (fitted_model, training_time_seconds)."""
    start = time.time()
    model.fit(X_train, y_train)
    elapsed = round(time.time() - start, 4)
    return model, elapsed
