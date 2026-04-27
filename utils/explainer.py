import numpy as np
import pandas as pd
import plotly.graph_objects as go


def explain_prediction(model, model_name: str, input_array, feature_names: list, class_names=None):
    """Return a dict with explanation text and optional figure."""
    result = {"text": "", "figure": None}

    if model_name == "KNN":
        k = model.n_neighbors
        result["text"] = (
            f"**KNN Explanation:** This prediction was determined by the **{k} nearest neighbors** "
            f"in the training set. The majority class among those {k} neighbors becomes the prediction."
        )

    elif model_name == "Decision Tree":
        result["text"] = _decision_tree_path(model, input_array, feature_names, class_names)

    elif model_name == "Random Forest":
        result["text"] = "**Random Forest:** Prediction is the majority vote of all decision trees."
        result["figure"] = _rf_feature_contrib(model, input_array, feature_names)

    elif model_name == "Logistic Regression":
        coefs = model.coef_
        if coefs.shape[0] == 1:
            coefs = coefs[0]
            contrib = coefs * input_array[0]
            result["figure"] = _coef_bar(contrib, feature_names, "Logistic Regression Feature Contribution")
        result["text"] = "**Logistic Regression:** The log-odds are a weighted sum of features."

    elif model_name == "SVM":
        if hasattr(model, "decision_function"):
            dist = model.decision_function(input_array.reshape(1, -1))[0]
            if np.isscalar(dist):
                result["text"] = (
                    f"**SVM:** Distance from the decision boundary: **{dist:.4f}**. "
                    f"Larger absolute values indicate higher confidence."
                )
            else:
                result["text"] = "**SVM:** Multi-class decision values: " + ", ".join(f"{d:.3f}" for d in dist)

    return result


def _decision_tree_path(model, input_array, feature_names, class_names):
    from sklearn.tree import _tree
    tree_ = model.tree_
    feature = tree_.feature
    threshold = tree_.threshold

    node = 0
    path_parts = []
    while feature[node] != _tree.TREE_LEAF:
        fname = feature_names[feature[node]] if feature_names else f"f{feature[node]}"
        thresh = threshold[node]
        val = input_array[0][feature[node]]
        direction = "<=" if val <= thresh else ">"
        path_parts.append(f"`{fname}` {direction} {thresh:.3f} (value={val:.3f})")
        node = tree_.children_left[node] if val <= thresh else tree_.children_right[node]

    leaf_values = tree_.value[node][0]
    pred_class = np.argmax(leaf_values)
    class_label = class_names[pred_class] if class_names else str(pred_class)
    if path_parts:
        path_str = "\n".join(f"→ {p}" for p in path_parts)
        return f"**Decision Path:**\n{path_str}\n\n→ **Predicted class: {class_label}**"
    return f"**Decision Path:** Single-node tree (no splits)\n\n→ **Predicted class: {class_label}**"


def _rf_feature_contrib(model, input_array, feature_names):
    importances = model.feature_importances_
    contrib = importances * np.abs(input_array[0])
    contrib = contrib / (contrib.sum() + 1e-9)
    top_n = min(10, len(feature_names))
    idx = np.argsort(contrib)[-top_n:]

    fig = go.Figure(go.Bar(
        x=contrib[idx],
        y=[feature_names[i] for i in idx],
        orientation="h",
        marker=dict(color=contrib[idx], colorscale="Reds"),
    ))
    fig.update_layout(
        title="Feature Contribution to This Prediction",
        xaxis_title="Contribution", template="plotly_dark", height=380,
    )
    return fig


def _coef_bar(contrib, feature_names, title):
    idx = np.argsort(np.abs(contrib))[-10:]
    fig = go.Figure(go.Bar(
        x=contrib[idx],
        y=[feature_names[i] for i in idx],
        orientation="h",
        marker=dict(color=contrib[idx], colorscale="RdBu"),
    ))
    fig.update_layout(title=title, xaxis_title="Contribution",
                      template="plotly_dark", height=380)
    return fig
