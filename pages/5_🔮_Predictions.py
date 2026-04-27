import streamlit as st
import numpy as np
import pandas as pd
import io

from utils.explainer import explain_prediction
from utils.styles import inject_global_css, page_header, render_sidebar_status

st.set_page_config(page_title="Predictions — ML Playground", page_icon="🔮", layout="wide", initial_sidebar_state="expanded")
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

.pred-result-card {
    background: linear-gradient(135deg, rgba(255,75,75,0.07), rgba(255,140,66,0.03));
    border: 1px solid rgba(255,75,75,0.22);
    border-radius: 16px; padding: 1.5rem 1.75rem; margin: 1rem 0;
}
.pred-label-row { display:flex; align-items:center; gap:0.75rem; margin-bottom:0.75rem; }
.pred-tag {
    font-size: 0.65rem; font-weight: 700; color: #FF4B4B;
    text-transform: uppercase; letter-spacing: 0.1em;
}
.pred-class { font-size: 1.8rem; font-weight: 900; color: #FAFAFA; }
.conf-bar-wrap { height: 6px; background: rgba(255,255,255,0.06); border-radius: 3px; margin: 0.5rem 0 0.25rem; overflow:hidden; }
.conf-bar { height:100%; border-radius:3px; background: linear-gradient(90deg, #FF4B4B, #FF8C42); transition: width 0.6s ease; }
.conf-label { font-size: 0.75rem; color: #6b7280; }

.sec-eyebrow {
    font-size: 0.62rem; font-weight: 700; color: #FF4B4B;
    text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.3rem;
}
.sec-heading {
    font-size: 1.1rem; font-weight: 800; color: #FAFAFA;
    letter-spacing: -0.01em; margin-bottom: 0.75rem;
}
.batch-hint {
    background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px; padding: 0.75rem 1rem;
    font-size: 0.8rem; color: #6b7280; margin-bottom: 1rem;
    font-family: monospace;
}
</style>
""", unsafe_allow_html=True)

page_header("Predictions", "Make single or batch predictions using your trained model.", "🔮")

if "training_results" not in st.session_state:
    st.markdown(
        '<div class="guard-box"><div style="font-size:1.5rem">⚠️</div>'
        '<div><div class="guard-title">No trained model found</div>'
        '<div class="guard-desc">Train a model first, then return here to make predictions.</div></div></div>',
        unsafe_allow_html=True,
    )
    if st.button("→ Go to Training", type="primary"):
        st.switch_page("pages/2_🎯_Train_Model.py")
    st.stop()

results        = st.session_state["training_results"]
task           = st.session_state.get("task", "classification")
trained_models = st.session_state.get("trained_models", list(results.keys()))
df_ds: pd.DataFrame = st.session_state.get("df", pd.DataFrame())
target_col     = st.session_state.get("target_col")

if task == "clustering":
    st.info("Clustering predictions assign cluster labels to new data points.")

model_name    = st.selectbox("Select model", trained_models)
model         = st.session_state.get(f"model_{model_name}")
scaler        = st.session_state.get(f"scaler_{model_name}")
feature_names = st.session_state.get(f"feature_names_{model_name}", [])

if model is None:
    st.error("Model not found in session. Please re-train the model.")
    st.stop()

class_names = None
if target_col and target_col in df_ds.columns:
    class_names = [str(c) for c in sorted(df_ds[target_col].unique())]

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_single, tab_batch = st.tabs(["🎯 Single Prediction", "📦 Batch Prediction"])

# ════════════════════════════════════════════════════════════════════════════
with tab_single:
    st.markdown('<div class="sec-eyebrow">Input</div><div class="sec-heading">Enter Feature Values</div>', unsafe_allow_html=True)

    feature_df = df_ds.drop(columns=[target_col]) if target_col and target_col in df_ds.columns else df_ds

    if st.button("🎲 Fill Random Sample"):
        sample_row = feature_df.sample(1).iloc[0]
        for fn in feature_names:
            if fn in sample_row.index:
                st.session_state[f"inp_{fn}"] = float(sample_row[fn])

    input_values = {}
    cols = st.columns(min(3, len(feature_names)))
    for i, fname in enumerate(feature_names):
        col = cols[i % len(cols)]
        with col:
            col_series  = feature_df[fname] if fname in feature_df.columns else pd.Series([0.0])
            default_val = st.session_state.get(f"inp_{fname}", float(col_series.mean()))
            input_values[fname] = st.number_input(
                fname, value=default_val, key=f"inp_{fname}", format="%.4f",
            )

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    if st.button("Predict →", type="primary", use_container_width=True):
        raw_input    = np.array([[input_values[fn] for fn in feature_names]])
        scaled_input = scaler.transform(raw_input) if scaler is not None else raw_input
        prediction   = model.predict(scaled_input)[0]

        if class_names and int(prediction) < len(class_names):
            pred_label = class_names[int(prediction)]
        else:
            pred_label = str(prediction)

        confidence       = None
        confidence_color = "#FF8C42"
        if hasattr(model, "predict_proba"):
            proba      = model.predict_proba(scaled_input)[0]
            confidence = float(np.max(proba)) * 100
            confidence_color = "#22c55e" if confidence >= 80 else "#f59e0b" if confidence >= 50 else "#ef4444"

        conf_pct  = f"{confidence:.1f}%" if confidence is not None else "N/A"
        conf_bar  = f"{confidence:.1f}" if confidence is not None else "0"

        st.markdown(
            f'<div class="pred-result-card">'
            f'<div class="pred-tag">Predicted Class</div>'
            f'<div class="pred-class">{pred_label}</div>'
            + (
                f'<div style="margin-top:0.75rem;">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.3rem;">'
                f'<span style="font-size:0.78rem;color:#9ca3af;">Confidence</span>'
                f'<span style="font-size:0.9rem;font-weight:700;color:{confidence_color};">{conf_pct}</span>'
                f'</div>'
                f'<div class="conf-bar-wrap"><div class="conf-bar" style="width:{conf_bar}%;background:{confidence_color};"></div></div>'
                f'</div>'
                if confidence is not None else ""
            ) +
            f'</div>',
            unsafe_allow_html=True,
        )

        if confidence is not None and class_names:
            with st.expander("Class Probabilities"):
                prob_df = pd.DataFrame({
                    "Class": class_names,
                    "Probability": [f"{p*100:.1f}%" for p in proba],
                })
                st.dataframe(prob_df, hide_index=True, use_container_width=True)

        st.markdown('<div class="sec-eyebrow" style="margin-top:1rem;">Explanation</div><div class="sec-heading">Why this prediction?</div>', unsafe_allow_html=True)
        expl = explain_prediction(model, model_name, scaled_input, feature_names, class_names)
        st.markdown(expl["text"])
        if expl["figure"] is not None:
            st.plotly_chart(expl["figure"], use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
with tab_batch:
    st.markdown('<div class="sec-eyebrow">Bulk</div><div class="sec-heading">Upload CSV for Batch Predictions</div>', unsafe_allow_html=True)

    st.markdown(
        f'<div class="batch-hint">Required columns: {", ".join(feature_names)}</div>',
        unsafe_allow_html=True,
    )

    batch_file = st.file_uploader("Upload CSV", type=["csv"], key="batch_upload")
    if batch_file:
        try:
            batch_df = pd.read_csv(batch_file)
        except Exception as e:
            st.error(f"Could not read CSV: {e}")
            st.stop()

        missing_cols = [fn for fn in feature_names if fn not in batch_df.columns]
        if missing_cols:
            st.error(f"Missing columns in your CSV: {missing_cols}")
            st.stop()

        X_batch = batch_df[feature_names].values
        if scaler is not None:
            X_batch = scaler.transform(X_batch)

        preds = model.predict(X_batch)
        if class_names:
            pred_labels = [class_names[int(p)] if int(p) < len(class_names) else str(p) for p in preds]
        else:
            pred_labels = [str(p) for p in preds]

        batch_df["prediction"] = pred_labels
        if hasattr(model, "predict_proba"):
            probas = model.predict_proba(X_batch)
            batch_df["confidence"] = [f"{np.max(p)*100:.1f}%" for p in probas]

        st.success(f"✓ Predicted {len(batch_df):,} rows successfully.")
        st.dataframe(batch_df, use_container_width=True)

        st.markdown('<div class="sec-eyebrow" style="margin-top:1rem;">Summary</div>', unsafe_allow_html=True)
        from utils.plots import plot_class_distribution
        st.plotly_chart(plot_class_distribution(batch_df["prediction"]), use_container_width=True)

        csv_out = batch_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Predictions CSV",
            data=csv_out,
            file_name="predictions.csv",
            mime="text/csv",
        )
