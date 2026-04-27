import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.comparison import build_comparison_table, recommend_model, pareto_frontier
from utils.plots import (
    plot_comparison_bar, plot_radar_chart, plot_tradeoff_scatter,
    plot_confusion_matrix, plot_roc_curve,
)
from utils.styles import inject_global_css, page_header, render_sidebar_status

st.set_page_config(page_title="Comparison — ML Playground", page_icon="⚖️", layout="wide", initial_sidebar_state="expanded")
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

.best-banner {
    display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;
    background: linear-gradient(135deg, rgba(255,75,75,0.08), rgba(255,140,66,0.04));
    border: 1px solid rgba(255,75,75,0.25);
    border-radius: 14px; padding: 1rem 1.5rem; margin-bottom: 1.25rem;
}
.best-trophy { font-size: 1.8rem; line-height: 1; }
.best-label  { font-size: 0.62rem; font-weight: 700; color: #FF4B4B;
               text-transform: uppercase; letter-spacing: 0.1em; }
.best-name   { font-size: 1.1rem; font-weight: 800; color: #FAFAFA; }
.best-pareto { font-size: 0.78rem; color: #6b7280; margin-top: 0.15rem; }
.best-pareto span { color: #FF8C42; font-weight: 600; }

.chart-section {
    background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px; padding: 1.25rem 1.5rem; margin-bottom: 1rem;
}
.chart-title {
    font-size: 0.88rem; font-weight: 700; color: #e5e7eb; margin-bottom: 0.75rem;
}
.sec-eyebrow {
    font-size: 0.62rem; font-weight: 700; color: #FF4B4B;
    text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.3rem;
}
.sec-heading {
    font-size: 1.2rem; font-weight: 800; color: #FAFAFA;
    letter-spacing: -0.01em; margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

page_header("Model Comparison", "Side-by-side analysis of every model you trained.", "⚖️")

if "training_results" not in st.session_state:
    st.markdown(
        '<div class="guard-box"><div style="font-size:1.5rem">⚠️</div>'
        '<div><div class="guard-title">No trained models found</div>'
        '<div class="guard-desc">Train at least 2 models in Compare Mode first.</div></div></div>',
        unsafe_allow_html=True,
    )
    if st.button("→ Go to Training", type="primary"):
        st.switch_page("pages/2_🎯_Train_Model.py")
    st.stop()

results = st.session_state["training_results"]
task    = st.session_state.get("task", "classification")

if len(results) < 2:
    st.markdown(
        '<div class="guard-box"><div style="font-size:1.5rem">ℹ️</div>'
        '<div><div class="guard-title">Only one model trained</div>'
        '<div class="guard-desc">Switch to <strong>Compare Mode</strong> and train multiple models to unlock this page.</div></div></div>',
        unsafe_allow_html=True,
    )
    if st.button("→ Go to Training", type="primary"):
        st.switch_page("pages/2_🎯_Train_Model.py")
    st.stop()

# ── Clustering path ───────────────────────────────────────────────────────────
if task == "clustering":
    st.markdown('<div class="sec-eyebrow">Clustering</div><div class="sec-heading">Comparison Summary</div>', unsafe_allow_html=True)
    rows = [
        {"Model": name, "Clusters": res["n_clusters"],
         "Inertia": f"{res['inertia']:.2f}", "Training Time": f"{res['training_time']:.4f}s"}
        for name, res in results.items()
    ]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    st.stop()

# ── Best model banner ─────────────────────────────────────────────────────────
best   = recommend_model(results)
pareto = pareto_frontier(results)
pareto_names = ", ".join(f'<span>{m}</span>' for m in pareto)

st.markdown(
    f'<div class="best-banner">'
    f'<div class="best-trophy">🏆</div>'
    f'<div>'
    f'<div class="best-label">Best Model by F1-Score</div>'
    f'<div class="best-name">{best}</div>'
    f'<div class="best-pareto">Pareto-efficient (accuracy + speed): {pareto_names}</div>'
    f'</div></div>',
    unsafe_allow_html=True,
)

# ── Summary table ─────────────────────────────────────────────────────────────
st.markdown('<div class="sec-eyebrow">Overview</div><div class="sec-heading">Summary Table</div>', unsafe_allow_html=True)
st.dataframe(build_comparison_table(results), use_container_width=True, hide_index=True)

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

# ── Metric bar charts (2×2) ───────────────────────────────────────────────────
st.markdown('<div class="sec-eyebrow">Metrics</div><div class="sec-heading">Performance Charts</div>', unsafe_allow_html=True)

r1c1, r1c2 = st.columns(2)
with r1c1:
    st.markdown('<div class="chart-section"><div class="chart-title">Accuracy</div>', unsafe_allow_html=True)
    st.plotly_chart(plot_comparison_bar(results, "accuracy"), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with r1c2:
    st.markdown('<div class="chart-section"><div class="chart-title">F1-Score</div>', unsafe_allow_html=True)
    st.plotly_chart(plot_comparison_bar(results, "f1"), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

r2c1, r2c2 = st.columns(2)
with r2c1:
    st.markdown('<div class="chart-section"><div class="chart-title">Training Time</div>', unsafe_allow_html=True)
    st.plotly_chart(plot_comparison_bar(results, "training_time"), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with r2c2:
    st.markdown('<div class="chart-section"><div class="chart-title">Radar — Multi-Metric Overview</div>', unsafe_allow_html=True)
    st.plotly_chart(plot_radar_chart(results), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Trade-off scatter ─────────────────────────────────────────────────────────
st.markdown('<div class="sec-eyebrow">Trade-off</div><div class="sec-heading">Accuracy vs Training Time</div>', unsafe_allow_html=True)
st.markdown('<div class="chart-section">', unsafe_allow_html=True)
st.plotly_chart(plot_tradeoff_scatter(results), use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Confusion matrix grid ─────────────────────────────────────────────────────
st.markdown('<div class="sec-eyebrow">Error Analysis</div><div class="sec-heading">Confusion Matrices</div>', unsafe_allow_html=True)
df_ds      = st.session_state.get("df", pd.DataFrame())
target_col = st.session_state.get("target_col")
class_names = None
if target_col and target_col in df_ds.columns:
    class_names = [str(c) for c in sorted(df_ds[target_col].unique())]

cm_cols = st.columns(len(results))
for col, (name, res) in zip(cm_cols, results.items()):
    with col:
        st.markdown(f'<div style="font-size:0.82rem;font-weight:700;color:#e5e7eb;margin-bottom:0.5rem;">{name}</div>', unsafe_allow_html=True)
        st.plotly_chart(
            plot_confusion_matrix(res["confusion_matrix"], class_names=class_names),
            use_container_width=True, key=f"cm_{name}",
        )

# ── ROC overlay ───────────────────────────────────────────────────────────────
roc_models = {n: r for n, r in results.items() if r.get("roc")}
if roc_models:
    st.markdown('<div class="sec-eyebrow">Binary Classification</div><div class="sec-heading">ROC Curves — Overlay</div>', unsafe_allow_html=True)
    colors = ["#FF4B4B", "#636EFA", "#00CC96", "#AB63FA", "#FFA15A", "#19D3F3"]
    fig = go.Figure()
    for i, (name, res) in enumerate(roc_models.items()):
        roc = res["roc"]
        fig.add_trace(go.Scatter(
            x=roc["fpr"], y=roc["tpr"],
            name=f"{name} (AUC = {roc['auc']:.3f})",
            line=dict(color=colors[i % len(colors)], width=2.5),
        ))
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1], name="Random Baseline",
        line=dict(dash="dash", color="#4b5563", width=1.5),
    ))
    fig.update_layout(
        xaxis_title="False Positive Rate", yaxis_title="True Positive Rate",
        template="plotly_dark", height=420, margin=dict(t=20, b=20, l=20, r=20),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(255,255,255,0.1)", borderwidth=1),
    )
    st.plotly_chart(fig, use_container_width=True)

# ── Navigation ────────────────────────────────────────────────────────────────
st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
if st.button("🔮 Make Predictions", type="primary"):
    st.switch_page("pages/5_🔮_Predictions.py")
