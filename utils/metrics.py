import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_curve, auc
)
from sklearn.model_selection import cross_val_score


def classification_metrics(model, X_test, y_test, X_train=None, y_train=None, cv_folds: int = 5):
    """Return dict of all classification metrics."""
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
    rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
    f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)
    cm = confusion_matrix(y_test, y_pred)

    cv_scores = None
    if X_train is not None and y_train is not None:
        X_all = np.vstack([X_train, X_test])
        y_all = np.concatenate([y_train, y_test])
        cv_scores = cross_val_score(model, X_all, y_all, cv=cv_folds, scoring="accuracy")

    # ROC (binary only)
    roc_data = None
    classes = np.unique(y_test)
    if len(classes) == 2 and hasattr(model, "predict_proba"):
        proba = model.predict_proba(X_test)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, proba)
        roc_auc = auc(fpr, tpr)
        roc_data = {"fpr": fpr, "tpr": tpr, "auc": roc_auc}

    return {
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1": f1,
        "confusion_matrix": cm,
        "cv_scores": cv_scores,
        "roc": roc_data,
        "y_pred": y_pred,
    }


def clustering_metrics(model, X):
    """Return inertia and labels for K-Means."""
    labels = model.labels_
    inertia = model.inertia_
    return {"labels": labels, "inertia": inertia, "n_clusters": model.n_clusters}


def compute_elbow_data(X, max_k: int = 10):
    """Compute inertia for k=2..max_k for elbow plot."""
    from sklearn.cluster import KMeans
    inertias = []
    ks = list(range(2, max_k + 1))
    for k in ks:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X)
        inertias.append(km.inertia_)
    return ks, inertias


def learning_curve_data(model, X_train, y_train, cv: int = 5):
    """Compute learning curve training/validation scores."""
    from sklearn.model_selection import learning_curve
    train_sizes, train_scores, val_scores = learning_curve(
        model, X_train, y_train,
        cv=cv, n_jobs=-1,
        train_sizes=np.linspace(0.2, 1.0, 5),
        scoring="accuracy",
    )
    return {
        "train_sizes": train_sizes,
        "train_mean": train_scores.mean(axis=1),
        "train_std": train_scores.std(axis=1),
        "val_mean": val_scores.mean(axis=1),
        "val_std": val_scores.std(axis=1),
    }
