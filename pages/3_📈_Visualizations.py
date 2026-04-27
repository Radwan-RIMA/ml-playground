import streamlit as st
import numpy as np
import pandas as pd

from utils.plots import (
    plot_confusion_matrix, plot_roc_curve, plot_feature_importance,
    plot_learning_curve, plot_prediction_distribution,
    plot_clusters_2d, plot_elbow, plot_decision_boundary,
)
from utils.metrics import compute_elbow_data, learning_curve_data
from utils.styles import inject_global_css, page_header, render_sidebar_status, metric_card

st.set_page_config(page_title="Visualizations — ML Playground", page_icon="📈", layout="wide", initial_sidebar_state="expanded")
inject_global_css()
render_sidebar_status()

st.markdown("""
<style>
.guard-box {
    display: flex; align-items: flex-start; gap: 1rem;
    background: rgba(255,180,0,0.06); border: 1px solid rgba(255,180,0,0.2);
    border-radius: 14px; padding: 1.25rem 1.5rem; margin-bottom: 1rem;
}
.guard-title { font-size: 0.95rem; font-weight: 700; color: #fbbf24; }
.guard-desc  { font-size: 0.82rem; color: #6b7280; margin-top: 0.2rem; }
.chart-section {
    background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px; padding: 1.25rem 1.5rem; margin-bottom: 1rem;
}
.chart-section-title {
    font-size: 0.9rem; font-weight: 700; color: #e5e7eb;
    margin-bottom: 0.75rem; display:flex; align-items:center; gap:0.5rem;
}
.cv-banner {
    display:flex; align-items:center; gap:0.75rem;
    background: rgba(99,102,241,0.07); border: 1px solid rgba(99,102,241,0.2);
    border-radius: 10px; padding: 0.65rem 1rem; margin-top:0.75rem;
    font-size: 0.83rem; color: #a5b4fc;
}
.cv-banner strong { color: #FAFAFA; }
</style>
""", unsafe_allow_html=True)

page_header("Visualizations", "Explore metrics, charts, and model behaviour in depth.", "📈")

if "training_results" not in st.session_state:
    st.markdown(
        '<div class="guard-box"><div style="font-size:1.5rem">⚠️</div>'
        '<div><div class="guard-title">No trained model found</div>'
        '<div class="guard-desc">Train a model first, then come back here.</div></div></div>',
        unsafe_allow_html=True,
    )
    if st.button("→ Go to Training", type="primary"):
        st.switch_page("pages/2_🎯_Train_Model.py")
    st.stop()

results       = st.session_state["training_results"]
task          = st.session_state.get("task", "classification")
trained_models = st.session_state.get("trained_models", list(results.keys()))

if len(trained_models) > 1:
    model_name = st.selectbox("Select model to visualize", trained_models)
else:
    model_name = trained_models[0]

res   = results[model_name]
model = st.session_state.get(f"model_{model_name}")

st.markdown(
    f'<div style="font-size:0.8rem;color:#6b7280;margin-bottom:1rem;">'
    f'Showing results for <strong style="color:#FAFAFA;">{model_name}</strong></div>',
    unsafe_allow_html=True,
)

# ════════════════════════════════════════════════════════════════════════════
# CLUSTERING
# ════════════════════════════════════════════════════════════════════════════
if task == "clustering":
    X            = st.session_state.get(f"cluster_X_{model_name}")
    feature_names = st.session_state.get(f"feature_names_{model_name}", [])

    m1, m2, m3 = st.columns(3)
    m1.markdown(metric_card(str(res["n_clusters"]), "Clusters", icon="🔵"), unsafe_allow_html=True)
    m2.markdown(metric_card(f"{res['inertia']:.2f}", "Inertia", icon="📉"), unsafe_allow_html=True)
    m3.markdown(metric_card(f"{res['training_time']:.4f}s", "Training Time", icon="⏱️"), unsafe_allow_html=True)

    if X is not None:
        st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
        st.plotly_chart(
            plot_clusters_2d(X, res["labels"], centroids=model.cluster_centers_, feature_names=feature_names),
            use_container_width=True,
        )
        with st.spinner("Computing elbow plot…"):
            ks, inertias = compute_elbow_data(X, max_k=10)
        st.plotly_chart(plot_elbow(ks, inertias), use_container_width=True)
    st.stop()

# ════════════════════════════════════════════════════════════════════════════
# CLASSIFICATION
# ════════════════════════════════════════════════════════════════════════════
X_train      = st.session_state.get(f"X_train_{model_name}")
X_test       = st.session_state.get(f"X_test_{model_name}")
y_train      = st.session_state.get(f"y_train_{model_name}")
y_test       = st.session_state.get(f"y_test_{model_name}")
feature_names = st.session_state.get(f"feature_names_{model_name}", [])

# ── Metric cards (4 cols — no more 5-col overflow) ───────────────────────────
m1, m2, m3, m4 = st.columns(4)
m1.markdown(metric_card(f"{res['accuracy']*100:.1f}%",  "Accuracy",  pct=res['accuracy']*100,  icon="🎯"), unsafe_allow_html=True)
m2.markdown(metric_card(f"{res['precision']*100:.1f}%", "Precision", pct=res['precision']*100, icon="🔍"), unsafe_allow_html=True)
m3.markdown(metric_card(f"{res['recall']*100:.1f}%",    "Recall",    pct=res['recall']*100,    icon="📡"), unsafe_allow_html=True)
m4.markdown(metric_card(f"{res['f1']*100:.1f}%",        "F1-Score",  pct=res['f1']*100,        icon="⚡"), unsafe_allow_html=True)

if res.get("cv_scores") is not None:
    cv = res["cv_scores"]
    st.markdown(
        f'<div class="cv-banner">📊 &nbsp;<strong>{len(cv)}-Fold Cross-Validation Score:</strong>'
        f'&nbsp; {cv.mean():.4f} ± {cv.std():.4f}'
        f'&nbsp; · &nbsp;Training Time: <strong>{res["training_time"]:.4f}s</strong></div>',
        unsafe_allow_html=True,
    )

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# ── Confusion Matrix + ROC ────────────────────────────────────────────────────
cm_col, roc_col = st.columns(2)

df_ds      = st.session_state.get("df", pd.DataFrame())
target_col = st.session_state.get("target_col")
class_names = None
if target_col and target_col in df_ds.columns:
    class_names = [str(c) for c in sorted(df_ds[target_col].unique())]

with cm_col:
    st.markdown('<div class="chart-section">', unsafe_allow_html=True)
    st.markdown('<div class="chart-section-title">🟦 Confusion Matrix</div>', unsafe_allow_html=True)
    normalize = st.toggle("Normalize values", key="cm_norm")
    st.plotly_chart(
        plot_confusion_matrix(res["confusion_matrix"], class_names=class_names, normalize=normalize),
        use_container_width=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

with roc_col:
    st.markdown('<div class="chart-section">', unsafe_allow_html=True)
    st.markdown('<div class="chart-section-title">📈 ROC Curve</div>', unsafe_allow_html=True)
    if res.get("roc"):
        st.plotly_chart(plot_roc_curve(res["roc"]), use_container_width=True)
    else:
        st.markdown(
            '<div style="padding:2rem;text-align:center;color:#4b5563;font-size:0.85rem;">'
            'ROC curve is available for<br><strong style="color:#9ca3af;">binary classification</strong> only.'
            '</div>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

# ── Prediction Distribution ───────────────────────────────────────────────────
st.markdown('<div class="chart-section">', unsafe_allow_html=True)
st.markdown('<div class="chart-section-title">📊 Prediction Distribution</div>', unsafe_allow_html=True)
st.plotly_chart(
    plot_prediction_distribution(y_test, res["y_pred"], class_names=class_names),
    use_container_width=True,
)
st.markdown('</div>', unsafe_allow_html=True)

# ── Feature Importance ────────────────────────────────────────────────────────
if hasattr(model, "feature_importances_"):
    st.markdown('<div class="chart-section">', unsafe_allow_html=True)
    st.markdown('<div class="chart-section-title">🔑 Feature Importance</div>', unsafe_allow_html=True)
    st.plotly_chart(
        plot_feature_importance(model.feature_importances_, feature_names),
        use_container_width=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ── Advanced (expanders) ──────────────────────────────────────────────────────
with st.expander("🗺️ Decision Boundary — PCA 2D projection"):
    if X_test is not None:
        with st.spinner("Computing decision boundary…"):
            try:
                st.plotly_chart(
                    plot_decision_boundary(model, X_test, y_test, feature_names=feature_names),
                    use_container_width=True,
                )
            except Exception:
                st.warning("Decision boundary could not be rendered for this model.")

with st.expander("📉 Learning Curve"):
    if X_train is not None and y_train is not None:
        with st.spinner("Computing learning curve…"):
            try:
                lc = learning_curve_data(model, X_train, y_train)
                st.plotly_chart(plot_learning_curve(lc), use_container_width=True)
            except Exception:
                st.warning("Learning curve could not be computed for this model.")

# ── Navigation ────────────────────────────────────────────────────────────────
st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
col_a, col_b = st.columns(2)
with col_a:
    if st.button("⚖️ Model Comparison", use_container_width=True):
        st.switch_page("pages/4_⚖️_Model_Comparison.py")
with col_b:
    if st.button("🔮 Make Predictions", use_container_width=True, type="primary"):
        st.switch_page("pages/5_🔮_Predictions.py")
