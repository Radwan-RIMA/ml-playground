import streamlit as st
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score

from utils.models import MODEL_REGISTRY, build_model, train_model
from utils.preprocessing import prepare_data, prepare_clustering_data
from utils.metrics import classification_metrics, clustering_metrics
from utils.styles import inject_global_css, page_header, render_sidebar_status

st.set_page_config(page_title="Train — ML Playground", page_icon="🎯", layout="wide", initial_sidebar_state="expanded")
inject_global_css()
render_sidebar_status()

st.markdown("""
<style>
.status-banner {
    display: flex; align-items: center; gap: 1rem;
    background: rgba(34,197,94,0.06); border: 1px solid rgba(34,197,94,0.2);
    border-radius: 12px; padding: 0.85rem 1.25rem; margin-bottom: 1.25rem;
}
.status-dot { width:8px; height:8px; border-radius:50%; background:#22c55e; flex-shrink:0; }
.status-text { font-size:0.85rem; color:#9ca3af; }
.status-text strong { color:#FAFAFA; }

.guard-box {
    display: flex; align-items: flex-start; gap: 1rem;
    background: rgba(255,180,0,0.06); border: 1px solid rgba(255,180,0,0.2);
    border-radius: 14px; padding: 1.25rem 1.5rem; margin-bottom: 1rem;
}
.guard-title { font-size: 0.95rem; font-weight: 700; color: #fbbf24; }
.guard-desc  { font-size: 0.82rem; color: #6b7280; margin-top: 0.2rem; }

.results-table-wrap {
    background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px; padding: 1rem; margin-top: 1rem;
}
.sec-label {
    font-size: 0.65rem; font-weight: 700; color: #FF4B4B;
    text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

page_header("Model Training", "Configure, train, and compare machine learning models.", "🎯")

if "df" not in st.session_state:
    st.markdown(
        '<div class="guard-box">'
        '<div style="font-size:1.5rem">⚠️</div>'
        '<div><div class="guard-title">No dataset loaded</div>'
        '<div class="guard-desc">Please select a dataset before training a model.</div></div>'
        '</div>',
        unsafe_allow_html=True,
    )
    if st.button("→ Go to Dataset", type="primary"):
        st.switch_page("pages/1_📊_Dataset.py")
    st.stop()

df: pd.DataFrame = st.session_state["df"]
target_col  = st.session_state.get("target_col")
task        = st.session_state.get("task", "classification")
dataset_name = st.session_state.get("dataset_name", "Dataset")

st.markdown(
    f'<div class="status-banner"><div class="status-dot"></div>'
    f'<div class="status-text">'
    f'<strong>{dataset_name}</strong> &nbsp;·&nbsp; '
    f'Task: <strong>{task.capitalize()}</strong> &nbsp;·&nbsp; '
    f'Shape: <strong>{df.shape[0]:,} × {df.shape[1]}</strong>'
    f'</div></div>',
    unsafe_allow_html=True,
)

available_models = {k: v for k, v in MODEL_REGISTRY.items() if v["task"] == task}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sec-label" style="padding:0.5rem 0.25rem 0.25rem;">Training Options</div>', unsafe_allow_html=True)
    split_map   = {"80 / 20": 0.20, "75 / 25": 0.25, "70 / 30": 0.30}
    split_label = st.radio("Train / Test Split", list(split_map.keys()), index=0)
    test_size   = split_map[split_label]
    scaling     = st.selectbox(
        "Feature Scaling", ["standard", "minmax", "none"],
        format_func=lambda x: {"standard": "StandardScaler", "minmax": "MinMaxScaler", "none": "None"}[x],
    )
    cv_folds = st.selectbox("Cross-validation Folds", [3, 5, 10], index=1)

# ── Mode & model selector ──────────────────────────────────────────────────────
mode = st.radio("Training Mode", ["Single Model", "Compare Models"], horizontal=True)
st.markdown("<div style='height:0.25rem'></div>", unsafe_allow_html=True)

if mode == "Single Model":
    model_name     = st.selectbox("Select Model", list(available_models.keys()))
    selected_models = [model_name]
else:
    selected_models = st.multiselect(
        "Select up to 3 models to compare",
        list(available_models.keys()),
        default=list(available_models.keys())[:2],
        max_selections=3,
    )

# ── Hyperparameter controls ────────────────────────────────────────────────────
model_params = {}
for mname in selected_models:
    info = MODEL_REGISTRY[mname]
    with st.expander(f"⚙️ {mname} — Hyperparameters", expanded=(len(selected_models) == 1)):
        params = {}
        for pname, pdef in info["params"].items():
            if pdef["type"] == "slider":
                val = st.slider(
                    pname,
                    min_value=float(pdef["min"])     if isinstance(pdef["min"],     float) else pdef["min"],
                    max_value=float(pdef["max"])     if isinstance(pdef["max"],     float) else pdef["max"],
                    value=float(pdef["default"])     if isinstance(pdef["default"], float) else pdef["default"],
                    step=float(pdef["step"])         if isinstance(pdef["step"],    float) else pdef["step"],
                    key=f"{mname}_{pname}",
                )
                params[pname] = int(val) if isinstance(pdef["default"], int) else val
            else:
                params[pname] = st.selectbox(
                    pname, pdef["options"],
                    index=pdef["options"].index(pdef["default"]),
                    key=f"{mname}_{pname}_sel",
                )
        model_params[mname] = params

# ── Train button ───────────────────────────────────────────────────────────────
st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
btn_label = "🚀 Train Model" if mode == "Single Model" else "🚀 Compare Models"
if st.button(btn_label, type="primary", use_container_width=True):
    if not selected_models:
        st.error("Please select at least one model.")
        st.stop()

    results = {}
    for mname in selected_models:
        with st.spinner(f"Training {mname}…"):
            model = build_model(mname, model_params[mname])
            if task == "clustering":
                X, feature_names, scaler = prepare_clustering_data(df, scaling=scaling)
                trained_model, elapsed = train_model(model, X, X)
                cmetrics = clustering_metrics(trained_model, X)
                results[mname] = {**cmetrics, "training_time": elapsed}
                st.session_state[f"cluster_X_{mname}"]    = X
                st.session_state[f"feature_names_{mname}"] = feature_names
            else:
                if target_col is None:
                    st.error("No target column set for classification.")
                    st.stop()
                X_train, X_test, y_train, y_test, feature_names, scaler = prepare_data(
                    df, target_col, test_size=test_size, scaling=scaling,
                )
                trained_model, elapsed = train_model(model, X_train, y_train)
                cmetrics = classification_metrics(
                    trained_model, X_test, y_test, X_train, y_train, cv_folds=cv_folds,
                )
                results[mname] = {**cmetrics, "training_time": elapsed}
                st.session_state[f"X_train_{mname}"]       = X_train
                st.session_state[f"X_test_{mname}"]        = X_test
                st.session_state[f"y_train_{mname}"]       = y_train
                st.session_state[f"y_test_{mname}"]        = y_test
                st.session_state[f"feature_names_{mname}"] = feature_names
                st.session_state[f"scaler_{mname}"]        = scaler
            st.session_state[f"model_{mname}"] = trained_model

    st.session_state["training_results"] = results
    st.session_state["trained_models"]   = selected_models
    st.session_state["mode"]             = mode

    st.success("✓ Training complete!")

    if task == "classification":
        rows = []
        for mname, res in results.items():
            cv = res.get("cv_scores")
            cv_str = f"{cv.mean():.3f} ± {cv.std():.3f}" if cv is not None else "—"
            rows.append({
                "Model":    mname,
                "Accuracy": f"{res['accuracy']*100:.1f}%",
                "F1-Score": f"{res['f1']*100:.1f}%",
                "CV Score": cv_str,
                "Time":     f"{res['training_time']:.4f}s",
            })
        st.markdown('<div class="sec-label" style="margin-top:1rem;">Results</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        cols_m = st.columns(len(results))
        for col, (mname, res) in zip(cols_m, results.items()):
            col.metric(f"{mname} — Inertia", f"{res['inertia']:.2f}")

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("📈 View Visualizations", use_container_width=True, type="primary"):
            st.switch_page("pages/3_📈_Visualizations.py")
    with col_b:
        if mode == "Compare Models" and st.button("⚖️ View Comparison", use_container_width=True):
            st.switch_page("pages/4_⚖️_Model_Comparison.py")
