import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from sklearn.decomposition import PCA


# ─── Confusion Matrix ────────────────────────────────────────────────────────

def plot_confusion_matrix(cm, class_names=None, normalize=False):
    if normalize:
        cm_plot = cm.astype(float) / cm.sum(axis=1, keepdims=True)
        fmt = ".2f"
    else:
        cm_plot = cm
        fmt = "d"

    labels = class_names if class_names else [str(i) for i in range(len(cm))]
    text = [[f"{cm_plot[i][j]:{fmt}}" for j in range(len(labels))] for i in range(len(labels))]

    fig = go.Figure(go.Heatmap(
        z=cm_plot, x=labels, y=labels,
        colorscale=[[0, "#1a1a2e"], [0.5, "#e94560"], [1, "#0f3460"]],
        text=text, texttemplate="%{text}",
        showscale=True,
    ))
    fig.update_layout(
        title="Confusion Matrix",
        xaxis_title="Predicted", yaxis_title="Actual",
        template="plotly_dark", height=450,
    )
    return fig


# ─── ROC Curve ───────────────────────────────────────────────────────────────

def plot_roc_curve(roc_data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=roc_data["fpr"], y=roc_data["tpr"],
        name=f'ROC (AUC = {roc_data["auc"]:.3f})',
        line=dict(color="#FF4B4B", width=2),
    ))
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1], name="Random Classifier",
        line=dict(dash="dash", color="gray"),
    ))
    fig.update_layout(
        title="ROC Curve", xaxis_title="False Positive Rate",
        yaxis_title="True Positive Rate", template="plotly_dark", height=400,
    )
    return fig


# ─── Feature Importance ──────────────────────────────────────────────────────

def plot_feature_importance(importances, feature_names, top_n=10):
    idx = np.argsort(importances)[-top_n:]
    fig = go.Figure(go.Bar(
        x=importances[idx], y=[feature_names[i] for i in idx],
        orientation="h",
        marker=dict(color=importances[idx], colorscale="Reds"),
    ))
    fig.update_layout(
        title=f"Top {top_n} Feature Importances",
        xaxis_title="Importance", template="plotly_dark", height=400,
    )
    return fig


# ─── Learning Curve ──────────────────────────────────────────────────────────

def plot_learning_curve(lc_data):
    sizes = lc_data["train_sizes"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sizes, y=lc_data["train_mean"], name="Training Score",
        line=dict(color="#FF4B4B"),
        error_y=dict(array=lc_data["train_std"], visible=True),
    ))
    fig.add_trace(go.Scatter(
        x=sizes, y=lc_data["val_mean"], name="Validation Score",
        line=dict(color="#00b4d8"),
        error_y=dict(array=lc_data["val_std"], visible=True),
    ))
    fig.update_layout(
        title="Learning Curve", xaxis_title="Training Set Size",
        yaxis_title="Accuracy", template="plotly_dark", height=400,
        yaxis=dict(range=[0, 1.05]),
    )
    return fig


# ─── Prediction Distribution ─────────────────────────────────────────────────

def plot_prediction_distribution(y_test, y_pred, class_names=None):
    labels = class_names if class_names else sorted(set(np.concatenate([y_test, y_pred])))
    actual_counts = [np.sum(y_test == c) for c in range(len(labels))] if class_names else \
                    [np.sum(np.array(y_test) == l) for l in labels]
    pred_counts = [np.sum(y_pred == c) for c in range(len(labels))] if class_names else \
                  [np.sum(np.array(y_pred) == l) for l in labels]

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Actual", x=[str(l) for l in labels], y=actual_counts,
                         marker_color="#636EFA"))
    fig.add_trace(go.Bar(name="Predicted", x=[str(l) for l in labels], y=pred_counts,
                         marker_color="#FF4B4B"))
    fig.update_layout(
        barmode="group", title="Actual vs Predicted Distribution",
        xaxis_title="Class", yaxis_title="Count",
        template="plotly_dark", height=380,
    )
    return fig


# ─── Cluster Visualization ───────────────────────────────────────────────────

def plot_clusters_2d(X, labels, centroids=None, feature_names=None):
    if X.shape[1] > 2:
        pca = PCA(n_components=2)
        X_2d = pca.fit_transform(X)
        x_label, y_label = "PC1", "PC2"
        if centroids is not None:
            centroids = pca.transform(centroids)
    else:
        X_2d = X
        x_label = feature_names[0] if feature_names else "Feature 1"
        y_label = feature_names[1] if feature_names else "Feature 2"

    df = pd.DataFrame({"x": X_2d[:, 0], "y": X_2d[:, 1], "cluster": labels.astype(str)})
    fig = px.scatter(df, x="x", y="y", color="cluster",
                     title="Cluster Visualization (PCA 2D)" if X.shape[1] > 2 else "Cluster Visualization",
                     labels={"x": x_label, "y": y_label},
                     template="plotly_dark", height=450)

    if centroids is not None:
        fig.add_trace(go.Scatter(
            x=centroids[:, 0], y=centroids[:, 1], mode="markers",
            marker=dict(symbol="x", size=14, color="white", line=dict(width=2)),
            name="Centroids",
        ))
    return fig


def plot_elbow(ks, inertias):
    fig = go.Figure(go.Scatter(
        x=ks, y=inertias, mode="lines+markers",
        line=dict(color="#FF4B4B", width=2),
        marker=dict(size=8),
    ))
    fig.update_layout(
        title="Elbow Plot (Inertia vs Number of Clusters)",
        xaxis_title="Number of Clusters (k)",
        yaxis_title="Inertia",
        template="plotly_dark", height=380,
    )
    return fig


# ─── Decision Boundary ───────────────────────────────────────────────────────

def plot_decision_boundary(model, X, y, feature_names=None):
    if X.shape[1] > 2:
        pca = PCA(n_components=2)
        X_2d = pca.fit_transform(X)
        xlabel, ylabel = "PC1", "PC2"

        h = 0.05
        x_min, x_max = X_2d[:, 0].min() - 1, X_2d[:, 0].max() + 1
        y_min, y_max = X_2d[:, 1].min() - 1, X_2d[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
        grid_2d = np.c_[xx.ravel(), yy.ravel()]
        grid_orig = pca.inverse_transform(grid_2d)
        Z = model.predict(grid_orig)
    else:
        X_2d = X
        xlabel = feature_names[0] if feature_names else "Feature 1"
        ylabel = feature_names[1] if feature_names else "Feature 2"

        h = 0.05
        x_min, x_max = X_2d[:, 0].min() - 1, X_2d[:, 0].max() + 1
        y_min, y_max = X_2d[:, 1].min() - 1, X_2d[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
        Z = model.predict(np.c_[xx.ravel(), yy.ravel()])

    Z = Z.reshape(xx.shape)

    fig = go.Figure()
    fig.add_trace(go.Contour(
        z=Z, x=np.arange(x_min, x_max, h), y=np.arange(y_min, y_max, h),
        colorscale="RdBu", opacity=0.4, showscale=False,
    ))
    classes = np.unique(y)
    colors = px.colors.qualitative.Plotly
    for i, cls in enumerate(classes):
        mask = y == cls
        fig.add_trace(go.Scatter(
            x=X_2d[mask, 0], y=X_2d[mask, 1], mode="markers",
            name=str(cls), marker=dict(color=colors[i % len(colors)], size=7, line=dict(width=1)),
        ))
    fig.update_layout(
        title="Decision Boundary" + (" (PCA 2D)" if X.shape[1] > 2 else ""),
        xaxis_title=xlabel, yaxis_title=ylabel,
        template="plotly_dark", height=450,
    )
    return fig


# ─── Comparison Charts ───────────────────────────────────────────────────────

def plot_comparison_bar(results: dict, metric: str = "accuracy"):
    names = list(results.keys())
    values = [results[n].get(metric, 0) * 100 for n in names]
    fig = px.bar(x=names, y=values, color=names,
                 labels={"x": "Model", "y": f"{metric.capitalize()} (%)"},
                 title=f"Model Comparison — {metric.capitalize()}",
                 template="plotly_dark", height=380)
    fig.update_layout(showlegend=False)
    return fig


def plot_radar_chart(results: dict):
    metrics = ["accuracy", "precision", "recall", "f1"]
    fig = go.Figure()
    colors = ["#FF4B4B", "#636EFA", "#00CC96", "#AB63FA", "#FFA15A"]
    for i, (name, res) in enumerate(results.items()):
        values = [res.get(m, 0) for m in metrics]
        values += values[:1]
        fig.add_trace(go.Scatterpolar(
            r=values, theta=metrics + [metrics[0]],
            fill="toself", name=name,
            line_color=colors[i % len(colors)],
        ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True, title="Model Performance Radar",
        template="plotly_dark", height=430,
    )
    return fig


def plot_tradeoff_scatter(results: dict):
    names = list(results.keys())
    accs = [results[n].get("accuracy", 0) * 100 for n in names]
    times = [results[n].get("training_time", 0) for n in names]
    fig = px.scatter(
        x=times, y=accs, text=names,
        labels={"x": "Training Time (s)", "y": "Accuracy (%)"},
        title="Accuracy vs Training Time Trade-off",
        template="plotly_dark", height=420,
    )
    fig.update_traces(textposition="top center", marker=dict(size=14, color="#FF4B4B"))
    return fig


# ─── Class Distribution ──────────────────────────────────────────────────────

def plot_class_distribution(series: pd.Series):
    counts = series.value_counts()
    fig = px.bar(x=counts.index.astype(str), y=counts.values,
                 labels={"x": "Class", "y": "Count"},
                 title="Class Distribution", template="plotly_dark",
                 color=counts.values, color_continuous_scale="Reds")
    fig.update_layout(showlegend=False, height=350)
    return fig


# ─── Correlation Heatmap ─────────────────────────────────────────────────────

def plot_correlation_heatmap(df: pd.DataFrame):
    num_df = df.select_dtypes(include="number")
    if num_df.shape[1] < 2:
        return None
    corr = num_df.corr()
    fig = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r",
                    title="Feature Correlation Heatmap", template="plotly_dark",
                    height=max(400, corr.shape[0] * 30))
    return fig


# ─── Missing Values Heatmap ──────────────────────────────────────────────────

def plot_missing_heatmap(df: pd.DataFrame):
    missing = df.isnull().astype(int)
    if missing.values.sum() == 0:
        return None
    fig = px.imshow(missing.T, color_continuous_scale=["#0E1117", "#FF4B4B"],
                    title="Missing Values Heatmap (red = missing)",
                    labels={"x": "Row", "y": "Column"},
                    template="plotly_dark", height=300)
    return fig
