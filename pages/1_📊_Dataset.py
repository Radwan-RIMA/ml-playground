import streamlit as st
import pandas as pd
import json
import os

from utils.data_loader import load_builtin_dataset, DATASET_OPTIONS
from utils.data_validator import validate_uploaded_csv, detect_column_types
from utils.preprocessing import handle_missing_values, encode_categoricals
from utils.plots import plot_class_distribution, plot_correlation_heatmap, plot_missing_heatmap
from utils.styles import inject_global_css, page_header, render_sidebar_status

st.set_page_config(page_title="Dataset — ML Playground", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
inject_global_css()
render_sidebar_status()

st.markdown("""
<style>
.ds-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1.1rem 1.1rem 0.6rem;
    margin-bottom: 0.5rem;
    min-height: 130px;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.ds-card:hover { border-color: rgba(255,75,75,0.3); box-shadow: 0 4px 20px rgba(255,75,75,0.07); }
.ds-card-title { font-size: 0.95rem; font-weight: 700; color: #FAFAFA; margin-bottom: 0.35rem; }
.ds-card-desc  { font-size: 0.77rem; color: #6b7280; line-height: 1.5; margin-bottom: 0.5rem; }
.ds-card-meta  { font-size: 0.7rem; color: #4b5563; font-weight: 500; }

.guard-box {
    display: flex; align-items: flex-start; gap: 1rem;
    background: rgba(255,180,0,0.06); border: 1px solid rgba(255,180,0,0.2);
    border-radius: 14px; padding: 1.25rem 1.5rem; margin-bottom: 1rem;
}
.guard-title { font-size: 0.95rem; font-weight: 700; color: #fbbf24; }
.guard-desc  { font-size: 0.82rem; color: #6b7280; margin-top: 0.2rem; }

.preview-header {
    font-size: 1rem; font-weight: 700; color: #FAFAFA;
    margin: 1.25rem 0 0.75rem;
    display: flex; align-items: center; gap: 0.5rem;
}
.preview-header::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, rgba(255,75,75,0.2), transparent);
    margin-left: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

page_header("Dataset Selection", "Choose a built-in dataset or upload your own CSV to get started.", "📊")

desc_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_datasets", "dataset_descriptions.json")
with open(desc_path) as f:
    DESCRIPTIONS = json.load(f)


def _show_preview(df: pd.DataFrame, target_col, task: str, key_suffix: str = ""):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", f"{df.shape[0]:,}")
    c2.metric("Columns", df.shape[1])
    c3.metric("Target", target_col or "None")
    c4.metric("Missing", int(df.isnull().sum().sum()))

    with st.expander("📋 Data Preview — first 10 rows", expanded=True):
        st.dataframe(df.head(10), use_container_width=True)

    with st.expander("📐 Feature Statistics"):
        st.dataframe(df.describe().round(3), use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        if target_col and target_col in df.columns:
            st.markdown('<div class="preview-header">Class Distribution</div>', unsafe_allow_html=True)
            st.plotly_chart(
                plot_class_distribution(df[target_col]),
                use_container_width=True, key=f"cls_dist_{key_suffix}",
            )
    with col_b:
        corr_fig = plot_correlation_heatmap(df)
        if corr_fig:
            st.markdown('<div class="preview-header">Correlation Heatmap</div>', unsafe_allow_html=True)
            st.plotly_chart(corr_fig, use_container_width=True, key=f"corr_{key_suffix}")

    miss_fig = plot_missing_heatmap(df)
    if miss_fig:
        st.markdown('<div class="preview-header">Missing Values Heatmap</div>', unsafe_allow_html=True)
        st.plotly_chart(miss_fig, use_container_width=True, key=f"miss_{key_suffix}")

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    if st.button("Proceed to Training →", type="primary", key=f"goto_train_{key_suffix}"):
        st.switch_page("pages/2_🎯_Train_Model.py")


# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_builtin, tab_upload = st.tabs(["🗂️ Built-in Datasets", "📤 Upload CSV"])

with tab_builtin:
    task_type = st.radio("Task Type", ["Classification", "Clustering"], horizontal=True)
    task_key = task_type.lower()
    dataset_map = DATASET_OPTIONS[task_key]

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    cols = st.columns(len(dataset_map))
    selected_key = None

    for col, (label, key) in zip(cols, dataset_map.items()):
        info = DESCRIPTIONS.get(key, {})
        meta_parts = []
        if info.get("rows"):     meta_parts.append(f"{info['rows']} rows")
        if info.get("features"): meta_parts.append(f"{info['features']} features")
        if info.get("classes"):  meta_parts.append(f"{info['classes']} classes")
        meta_str = " · ".join(meta_parts)

        with col:
            st.markdown(
                f'<div class="ds-card">'
                f'<div class="ds-card-title">{label}</div>'
                f'<div class="ds-card-desc">{info.get("description", "")}</div>'
                f'<div class="ds-card-meta">{meta_str}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            if st.button("Select", key=f"sel_{key}", use_container_width=True):
                selected_key = key

    first_key = list(dataset_map.values())[0]
    if "chosen_dataset_key" not in st.session_state:
        st.session_state["chosen_dataset_key"] = first_key
    if selected_key:
        st.session_state["chosen_dataset_key"] = selected_key

    chosen = st.session_state["chosen_dataset_key"]
    chosen_task = DESCRIPTIONS.get(chosen, {}).get("task", "classification")
    if chosen_task != task_key:
        chosen = first_key
        st.session_state["chosen_dataset_key"] = chosen

    st.divider()
    chosen_name = DESCRIPTIONS.get(chosen, {}).get("name", chosen)
    st.markdown(f'<div class="preview-header">Preview: {chosen_name}</div>', unsafe_allow_html=True)

    with st.spinner("Loading dataset..."):
        df, target_col, task = load_builtin_dataset(chosen)

    st.session_state["df"] = df
    st.session_state["target_col"] = target_col
    st.session_state["task"] = task
    st.session_state["dataset_name"] = chosen_name

    _show_preview(df, target_col, task, key_suffix="builtin")

with tab_upload:
    uploaded = st.file_uploader("Upload a CSV file (max 5 MB)", type=["csv"])
    if uploaded:
        try:
            df_upload = pd.read_csv(uploaded)
        except Exception as e:
            st.error(f"Could not read CSV: {e}")
            st.stop()

        valid, errors = validate_uploaded_csv(df_upload)
        if not valid:
            for err in errors:
                st.error(err)
            st.stop()

        col_types, missing_counts = detect_column_types(df_upload)
        total_missing = sum(missing_counts.values())
        st.success(f"✓ File loaded — {df_upload.shape[0]:,} rows × {df_upload.shape[1]} columns")

        target_upload = st.selectbox("Select target column", df_upload.columns.tolist())
        task_upload   = st.radio("Task", ["classification", "clustering"], horizontal=True, key="upload_task")

        if total_missing > 0:
            st.warning(f"Found {total_missing} missing values.")
            mv_strategy = st.selectbox("Handle missing values", ["mean", "median", "mode", "drop"])
            df_upload = handle_missing_values(df_upload, strategy=mv_strategy)

        cat_cols = [c for c, t in col_types.items() if t == "categorical" and c != target_upload]
        if cat_cols:
            st.info(f"Categorical columns detected: {', '.join(cat_cols)}")
            enc = st.selectbox("Encoding method", ["label", "onehot"])
            df_upload = encode_categoricals(df_upload, target_upload, method=enc)

        if st.button("Use This Dataset", type="primary"):
            st.session_state["df"] = df_upload
            st.session_state["target_col"] = target_upload if task_upload == "classification" else None
            st.session_state["task"] = task_upload
            st.session_state["dataset_name"] = uploaded.name
            st.success("Dataset saved — proceed to Train Model →")

        _show_preview(
            df_upload,
            target_upload if task_upload == "classification" else None,
            task_upload,
            key_suffix="upload",
        )
