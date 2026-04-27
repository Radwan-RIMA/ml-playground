import streamlit as st
import pandas as pd

from utils.styles import inject_global_css, page_header, render_sidebar_status

st.set_page_config(page_title="About — ML Playground", page_icon="📖", layout="wide", initial_sidebar_state="expanded")
inject_global_css()
render_sidebar_status()

st.markdown("""
<style>
.model-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px; padding: 1.25rem 1.5rem; margin-bottom: 0.75rem;
    transition: border-color 0.2s;
}
.model-card:hover { border-color: rgba(255,75,75,0.25); }
.model-card-header { display:flex; align-items:center; gap:0.6rem; margin-bottom:0.5rem; }
.model-icon-box {
    width:36px; height:36px; border-radius:10px;
    background: linear-gradient(135deg, rgba(255,75,75,0.12), rgba(255,140,66,0.06));
    border: 1px solid rgba(255,75,75,0.2);
    display:flex; align-items:center; justify-content:center; font-size:1rem; flex-shrink:0;
}
.model-name { font-size:0.95rem; font-weight:700; color:#FAFAFA; }
.model-desc { font-size:0.82rem; color:#6b7280; line-height:1.6; margin-bottom:0.5rem; }
.model-when { font-size:0.78rem; color:#9ca3af; }
.model-when strong { color:#FF8C42; }

.tech-row {
    display:grid; grid-template-columns:1fr 1fr 1fr; gap:0.75rem; margin-bottom:1rem;
}
.tech-card {
    background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px; padding: 1rem;
}
.tech-lib  { font-size:0.9rem; font-weight:700; color:#FAFAFA; }
.tech-ver  { font-size:0.7rem; color:#FF4B4B; font-weight:600; margin:0.15rem 0 0.35rem; }
.tech-desc { font-size:0.77rem; color:#6b7280; line-height:1.5; }

.param-card {
    background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px; padding: 1rem 1.25rem; margin-bottom: 0.6rem;
}
.param-name { font-size:0.88rem; font-weight:700; color:#FF8C42; margin-bottom:0.3rem; }
.param-desc { font-size:0.8rem; color:#6b7280; line-height:1.6; }

.future-card {
    background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px; padding: 1rem 1.25rem; margin-bottom: 0.6rem;
    display:flex; align-items:flex-start; gap:0.85rem;
}
.future-icon {
    width:38px; height:38px; border-radius:10px; flex-shrink:0;
    background: rgba(255,75,75,0.08); border:1px solid rgba(255,75,75,0.15);
    display:flex; align-items:center; justify-content:center; font-size:1.1rem;
}
.future-title { font-size:0.88rem; font-weight:700; color:#FAFAFA; margin-bottom:0.2rem; }
.future-desc  { font-size:0.78rem; color:#6b7280; line-height:1.5; }

.sec-eyebrow {
    font-size:0.62rem; font-weight:700; color:#FF4B4B;
    text-transform:uppercase; letter-spacing:0.12em; margin-bottom:0.3rem;
}
.sec-heading {
    font-size:1.3rem; font-weight:800; color:#FAFAFA;
    letter-spacing:-0.01em; margin-bottom:1rem;
}
</style>
""", unsafe_allow_html=True)

page_header("About & Documentation", "Everything you need to know about ML Playground.", "📖")

tab_models, tab_tech, tab_guide, tab_future = st.tabs([
    "🤖 Model Guide", "🛠️ Tech Stack", "📐 Hyperparameter Guide", "🚀 Future Plans",
])

# ════════════════════════════════════════════════════════════════════════════
with tab_models:
    st.markdown('<div class="sec-eyebrow">Algorithms</div><div class="sec-heading">How Each Model Works</div>', unsafe_allow_html=True)

    models_info = [
        ("🔵", "K-Nearest Neighbors",
         "KNN classifies a point by looking at its K nearest neighbors and taking a majority vote. Simple, intuitive, non-parametric — but slow at prediction time on large datasets since it stores all training examples.",
         "Small to medium datasets · Irregular decision boundaries · When training speed > prediction speed"),
        ("📉", "Logistic Regression",
         "Despite its name, it's a classification algorithm. It models class probability using a sigmoid applied to a linear combination of features. Fast, interpretable, and works well when classes are linearly separable.",
         "Linearly separable data · When you need probability outputs · Interpretability-critical domains"),
        ("🌳", "Decision Tree",
         "Recursively splits data on the most informative features, creating a tree of if-then rules. Highly interpretable — you can follow the path to understand any prediction. Prone to overfitting without depth limits.",
         "When explainability matters · Non-linear problems · Mixed feature types"),
        ("🌲", "Random Forest",
         "Trains many decision trees on random data subsets then aggregates their votes. This ensemble drastically reduces variance compared to a single tree and usually achieves the best accuracy of the group.",
         "Best default for tabular data · High-dimensional data · When accuracy > interpretability"),
        ("✂️", "Support Vector Machine",
         "Finds the hyperplane that maximises margin between classes. With the RBF kernel, it separates non-linear data by mapping to higher dimensions. Powerful but slower on large datasets.",
         "High-dimensional data (text, images) · Well-separated classes · Small to medium datasets"),
        ("🔵", "K-Means Clustering",
         "Partitions data into K clusters by iteratively assigning points to the nearest centroid and recomputing centroids. Requires specifying K in advance — use the Elbow Plot to choose a good value.",
         "Discovering natural groupings · Customer segmentation · Pre-supervised exploration"),
    ]

    for icon, name, desc, when in models_info:
        st.markdown(
            f'<div class="model-card">'
            f'<div class="model-card-header">'
            f'<div class="model-icon-box">{icon}</div>'
            f'<div class="model-name">{name}</div>'
            f'</div>'
            f'<div class="model-desc">{desc}</div>'
            f'<div class="model-when"><strong>Best for:</strong> {when}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

# ════════════════════════════════════════════════════════════════════════════
with tab_tech:
    st.markdown('<div class="sec-eyebrow">Stack</div><div class="sec-heading">Technologies Used</div>', unsafe_allow_html=True)

    tech = [
        ("Streamlit",           "1.28.0", "Web framework — builds the entire interactive UI"),
        ("scikit-learn",        "1.3.0",  "All ML models, preprocessing pipelines, and metrics"),
        ("Plotly",              "5.17.0", "Interactive, publication-quality visualizations"),
        ("Pandas",              "2.1.0",  "Data manipulation, cleaning, and display"),
        ("NumPy",               "1.24.0", "Numerical computing and array operations"),
        ("Matplotlib / Seaborn","3.7 / 0.12", "Supplementary static plots and styling"),
    ]

    r1 = st.columns(3)
    r2 = st.columns(3)
    for i, (lib, ver, purpose) in enumerate(tech):
        col = (r1 + r2)[i]
        with col:
            st.markdown(
                f'<div class="tech-card">'
                f'<div class="tech-lib">{lib}</div>'
                f'<div class="tech-ver">v{ver}</div>'
                f'<div class="tech-desc">{purpose}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sec-eyebrow">Structure</div><div class="sec-heading">Project Layout</div>', unsafe_allow_html=True)
    st.code("""
ml-playground/
├── app.py                          # Home page
├── pages/
│   ├── 1_📊_Dataset.py             # Dataset selection & preview
│   ├── 2_🎯_Train_Model.py         # Model training
│   ├── 3_📈_Visualizations.py      # Single-model visualizations
│   ├── 4_⚖️_Model_Comparison.py    # Multi-model comparison
│   ├── 5_🔮_Predictions.py         # Make predictions
│   └── 6_📖_About.py               # This page
├── utils/
│   ├── styles.py       # Global CSS + UI helpers
│   ├── data_loader.py  # Built-in dataset loader
│   ├── data_validator.py
│   ├── preprocessing.py
│   ├── models.py       # Model registry & factory
│   ├── metrics.py      # Metric computations
│   ├── plots.py        # All Plotly charts
│   ├── explainer.py    # Prediction explanations
│   └── comparison.py   # Comparison logic
├── data/sample_datasets/
├── .streamlit/config.toml
└── requirements.txt
    """, language="text")

# ════════════════════════════════════════════════════════════════════════════
with tab_guide:
    st.markdown('<div class="sec-eyebrow">Tuning</div><div class="sec-heading">Hyperparameter Guide</div>', unsafe_allow_html=True)

    params = [
        ("n_neighbors", "KNN",
         "Number of neighbours to vote on classification. Low → complex boundary (overfitting). High → smooth boundary (underfitting). Start with 5 and tune using the learning curve."),
        ("C", "Logistic Regression / SVM",
         "Regularisation strength. Low C → more regularisation (simpler model). High C → fits training data harder (risk of overfitting). Default: 1.0."),
        ("max_depth", "Decision Tree / Random Forest",
         "Maximum tree depth. Low → simple and underfit. High → complex and overfit. Use the learning curve to find the sweet spot."),
        ("n_estimators", "Random Forest",
         "Number of trees in the forest. More trees → better accuracy but slower. Diminishing returns past ~100. Start with 100."),
        ("kernel", "SVM",
         "rbf works for most cases. linear is fast for high-dimensional text. poly captures polynomial relationships but is slower."),
        ("n_clusters", "K-Means",
         "Number of clusters to form. Use the Elbow Plot — look for the point where inertia stops dropping sharply. That is your optimal K."),
    ]

    for param, model_hint, explanation in params:
        st.markdown(
            f'<div class="param-card">'
            f'<div class="param-name">{param} <span style="font-size:0.7rem;color:#4b5563;font-weight:500;">({model_hint})</span></div>'
            f'<div class="param-desc">{explanation}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

# ════════════════════════════════════════════════════════════════════════════
with tab_future:
    st.markdown('<div class="sec-eyebrow">Roadmap</div><div class="sec-heading">Planned Features</div>', unsafe_allow_html=True)

    future = [
        ("🧠", "Neural Networks",     "Add MLP classifier with customisable layers using Keras or PyTorch."),
        ("⏱️", "Time Series",         "LSTM and ARIMA models for forecasting and temporal pattern recognition."),
        ("📝", "Text Classification", "TF-IDF + Naive Bayes / SVM pipeline for NLP classification tasks."),
        ("🔍", "AutoML",              "Automatic hyperparameter search with Optuna — best config in one click."),
        ("📊", "SHAP Values",         "Advanced feature explanations using SHAP for any model type."),
        ("☁️", "Cloud Deploy",        "One-click deploy to Streamlit Community Cloud with a shareable URL."),
    ]

    for icon, title, desc in future:
        st.markdown(
            f'<div class="future-card">'
            f'<div class="future-icon">{icon}</div>'
            f'<div><div class="future-title">{title}</div>'
            f'<div class="future-desc">{desc}</div></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;'
    'gap:0.5rem;padding:1rem 0.25rem 0.5rem;border-top:1px solid rgba(255,255,255,0.06);margin-top:2rem;">'
    '<div style="font-size:0.77rem;color:#374151;">'
    '<strong style="color:#9ca3af;">ML Playground</strong> &nbsp;·&nbsp; '
    'Built by <strong style="color:#9ca3af;">Radwan Rima</strong> &nbsp;·&nbsp; '
    'Streamlit · scikit-learn · Plotly'
    '</div>'
    '<a style="display:inline-block;padding:0.38rem 1rem;background:linear-gradient(135deg,#FF4B4B,#FF8C42);'
    'color:#fff;text-decoration:none;border-radius:20px;font-size:0.73rem;font-weight:700;" '
    'href="https://github.com" target="_blank">⭐ Star on GitHub</a>'
    '</div>',
    unsafe_allow_html=True,
)
