import streamlit as st
from utils.styles import inject_global_css, render_sidebar_status

st.set_page_config(
    page_title="ML Playground",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()
render_sidebar_status()

st.markdown("""
<style>
/* ── Global page padding ──────────────────────────────────────────────────── */
.block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; }

/* ── Hero card (wraps the two columns) ───────────────────────────────────── */
[data-testid="stHorizontalBlock"]:first-of-type {
    background: linear-gradient(135deg, #0d1117 0%, #111827 55%, #0f1f3d 100%);
    border: 1px solid rgba(255,75,75,0.2);
    border-radius: 22px;
    padding: 1.5rem 2rem 2rem;
    margin-bottom: 3rem;
    box-shadow: 0 24px 80px rgba(0,0,0,0.45), 0 0 0 1px rgba(255,255,255,0.03);
    position: relative;
    overflow: hidden;
}
[data-testid="stHorizontalBlock"]:first-of-type::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(255,75,75,0.07), transparent 70%);
    pointer-events: none;
}

/* ── Hero typography ──────────────────────────────────────────────────────── */
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(255,75,75,0.1);
    border: 1px solid rgba(255,75,75,0.28);
    border-radius: 30px;
    padding: 5px 14px;
    font-size: 0.7rem;
    font-weight: 700;
    color: #FF4B4B;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 1.1rem;
}
.hero-title {
    font-size: 3.6rem;
    font-weight: 900;
    line-height: 1.05;
    margin: 0 0 1rem;
    color: #FAFAFA;
    letter-spacing: -0.02em;
}
.hero-accent {
    background: linear-gradient(135deg, #FF4B4B 0%, #FF8C42 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 1.1rem;
    color: #c8cdd6;
    line-height: 1.7;
    margin-bottom: 1.5rem;
    max-width: 480px;
}
.hbadge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 30px;
    padding: 5px 11px;
    font-size: 0.74rem;
    color: #9ca3af;
    font-weight: 500;
    white-space: nowrap;
}
.trust-row {
    display: flex;
    gap: 1.25rem;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(255,255,255,0.06);
}
.trust-item {
    font-size: 0.76rem;
    color: #4b5563;
    display: flex;
    align-items: center;
    gap: 0.3rem;
}
.trust-item::before {
    content: '✓';
    color: #22c55e;
    font-weight: 700;
}

/* ── Right panel ──────────────────────────────────────────────────────────── */
.hero-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.25rem 1.4rem;
    margin-bottom: 0.75rem;
}
.panel-label {
    font-size: 0.62rem;
    font-weight: 700;
    color: #FF4B4B;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.9rem;
}
.mini-stats {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.55rem;
}
.mini-stat {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 0.8rem 0.5rem;
    text-align: center;
}
.mini-stat-num {
    font-size: 1.75rem;
    font-weight: 900;
    background: linear-gradient(135deg, #FF4B4B, #FF8C42);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}
.mini-stat-lbl {
    font-size: 0.62rem;
    color: #4b5563;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
    margin-top: 0.25rem;
}
.check-item {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    padding: 0.5rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    font-size: 0.83rem;
    color: #9ca3af;
    font-weight: 500;
}
.check-item:last-child { border-bottom: none; }
.check-icon {
    width: 18px; height: 18px;
    border-radius: 50%;
    background: rgba(34,197,94,0.1);
    border: 1px solid rgba(34,197,94,0.3);
    color: #22c55e;
    font-size: 0.6rem;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; font-weight: 900;
}

/* ── Section layout ───────────────────────────────────────────────────────── */
.sec-block  { margin-top: 0.75rem; margin-bottom: 1.5rem; }
.sec-eyebrow {
    font-size: 0.65rem;
    font-weight: 700;
    color: #FF4B4B;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    margin-bottom: 0.4rem;
}
.sec-title {
    font-size: 1.9rem;
    font-weight: 900;
    color: #FAFAFA;
    letter-spacing: -0.02em;
    line-height: 1.15;
    margin-bottom: 0.4rem;
}
.sec-sub {
    font-size: 0.95rem;
    color: #6b7280;
    margin-bottom: 1.5rem;
    line-height: 1.6;
}
.sec-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,75,75,0.2), transparent);
    margin: 2.5rem 0;
}

/* ── Feature cards ────────────────────────────────────────────────────────── */
.feat-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.5rem;
    height: 100%;
    transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
}
.feat-card:hover {
    border-color: rgba(255,75,75,0.3);
    box-shadow: 0 8px 32px rgba(255,75,75,0.08);
    transform: translateY(-2px);
}
.feat-icon-box {
    width: 46px; height: 46px;
    border-radius: 12px;
    background: linear-gradient(135deg, rgba(255,75,75,0.12), rgba(255,140,66,0.06));
    border: 1px solid rgba(255,75,75,0.2);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.35rem;
    margin-bottom: 1rem;
    transition: transform 0.2s;
}
.feat-card:hover .feat-icon-box { transform: scale(1.08); }
.feat-title { font-size: 0.95rem; font-weight: 700; color: #FAFAFA; margin-bottom: 0.4rem; }
.feat-desc  { font-size: 0.81rem; color: #6b7280; line-height: 1.65; }

/* ── Step cards ───────────────────────────────────────────────────────────── */
.step-card {
    display: flex;
    gap: 1rem;
    align-items: flex-start;
    padding: 0.85rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.step-card:last-child { border-bottom: none; }
.step-num {
    min-width: 28px; height: 28px;
    border-radius: 8px;
    background: linear-gradient(135deg, #FF4B4B, #FF8C42);
    color: #fff; font-weight: 800; font-size: 0.78rem;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; letter-spacing: -0.02em;
}
.step-title { font-size: 0.88rem; font-weight: 700; color: #e5e7eb; margin-bottom: 0.18rem; }
.step-desc  { font-size: 0.77rem; color: #6b7280; line-height: 1.55; }

/* ── What's Included tags ─────────────────────────────────────────────────── */
.inc-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 1.25rem 1.4rem;
}
.tag-lbl {
    font-size: 0.62rem; color: #FF4B4B;
    text-transform: uppercase; letter-spacing: 0.12em;
    font-weight: 700; margin: 1rem 0 0.45rem;
}
.tag-lbl:first-child { margin-top: 0; }
.tag {
    display: inline-flex;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 3px 11px;
    font-size: 0.74rem;
    color: #9ca3af;
    margin: 2px; font-weight: 500;
    transition: all 0.15s;
}
.tag:hover {
    background: rgba(255,75,75,0.07);
    border-color: rgba(255,75,75,0.2);
    color: #fca5a5;
}

/* ── Bottom CTA band ─────────────────────────────────────────────────────── */
.cta-band {
    background: linear-gradient(135deg, #0d1117 0%, #111827 40%, #0f1f3d 100%);
    border: 1px solid rgba(255,75,75,0.22);
    border-radius: 22px;
    padding: 3.5rem 2rem 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin-bottom: 1.25rem;
    box-shadow: 0 20px 80px rgba(255,75,75,0.07), 0 0 0 1px rgba(255,255,255,0.02);
}
.cta-glow {
    position: absolute;
    top: -80px; left: 50%; transform: translateX(-50%);
    width: 500px; height: 300px;
    background: radial-gradient(ellipse, rgba(255,75,75,0.12), transparent 70%);
    pointer-events: none;
}
.cta-eyebrow {
    display: inline-block;
    background: rgba(255,75,75,0.1);
    border: 1px solid rgba(255,75,75,0.28);
    border-radius: 30px;
    padding: 4px 14px;
    font-size: 0.68rem;
    font-weight: 700;
    color: #FF4B4B;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 1.1rem;
}
.cta-title {
    font-size: 2.8rem;
    font-weight: 900;
    color: #FAFAFA;
    letter-spacing: -0.025em;
    line-height: 1.1;
    margin-bottom: 1rem;
    background: linear-gradient(180deg, #FFFFFF 0%, #9ca3af 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.cta-sub {
    font-size: 1rem;
    color: #6b7280;
    line-height: 1.7;
    margin-bottom: 0.5rem;
}

/* ── Footer ───────────────────────────────────────────────────────────────── */
.footer-wrap {
    display: flex; align-items: center;
    justify-content: space-between; flex-wrap: wrap; gap: 0.5rem;
    padding: 1.1rem 0.25rem 0.5rem;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin-top: 2rem;
}
.footer-left  { font-size: 0.77rem; color: #374151; }
.footer-left strong { color: #9ca3af; font-weight: 600; }
.footer-link  {
    display: inline-block;
    padding: 0.38rem 1rem;
    background: linear-gradient(135deg, #FF4B4B, #FF8C42);
    color: #fff; text-decoration: none;
    border-radius: 20px; font-size: 0.73rem; font-weight: 700;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════════════
hero_l, hero_r = st.columns([1.15, 1])

with hero_l:
    st.markdown('<div style="height:0.75rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-eyebrow">🤖 No-Code Machine Learning</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-title">ML <span class="hero-accent">Playground</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="hero-sub">Train, visualize, and compare machine learning models — '
        'interactively, without writing a single line of code.</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="display:flex;gap:0.45rem;flex-wrap:nowrap;margin-bottom:1.4rem;">'
        '<span class="hbadge">🎓 Students</span>'
        '<span class="hbadge">📊 Analysts</span>'
        '<span class="hbadge">🏆 Interview Prep</span>'
        '<span class="hbadge">🔬 Researchers</span>'
        '</div>',
        unsafe_allow_html=True,
    )
    if st.button("🚀 Get Started →", type="primary", key="hero_cta"):
        st.switch_page("pages/1_📊_Dataset.py")
    st.markdown(
        '<div class="trust-row">'
        '<span class="trust-item">100% Free</span>'
        '<span class="trust-item">No signup needed</span>'
        '<span class="trust-item">Open source</span>'
        '</div>',
        unsafe_allow_html=True,
    )

with hero_r:
    st.markdown('<div style="height:0.75rem"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-panel">'
        '<div class="panel-label">By the Numbers</div>'
        '<div class="mini-stats">'
        '<div class="mini-stat"><div class="mini-stat-num">6</div><div class="mini-stat-lbl">ML Models</div></div>'
        '<div class="mini-stat"><div class="mini-stat-num">6</div><div class="mini-stat-lbl">Datasets</div></div>'
        '<div class="mini-stat"><div class="mini-stat-num">15+</div><div class="mini-stat-lbl">Visualizations</div></div>'
        '<div class="mini-stat"><div class="mini-stat-num">10+</div><div class="mini-stat-lbl">Algorithms</div></div>'
        '</div></div>',
        unsafe_allow_html=True,
    )
    checks = [
        "Upload your own CSV or pick a built-in dataset",
        "Tune hyperparameters with live sliders",
        "Compare up to 3 models side-by-side",
        "Download predictions as CSV",
        "Explore 15+ interactive visualizations",
    ]
    rows = "".join(
        f'<div class="check-item"><div class="check-icon">✓</div>{c}</div>'
        for c in checks
    )
    st.markdown(
        f'<div class="hero-panel"><div class="panel-label">What You Can Do</div>{rows}</div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# FEATURES
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    '<div class="sec-eyebrow">Features</div>'
    '<div class="sec-title">Everything in One Place</div>'
    '<div class="sec-sub">From raw CSV to trained model — no environment setup, no code, no friction.</div>',
    unsafe_allow_html=True,
)

features = [
    ("🎓", "Learn by Doing",
     "Interact with real ML algorithms using sliders and dropdowns. See instantly how each hyperparameter changes the model."),
    ("⚡", "Instant Visual Feedback",
     "Every change re-trains in seconds. Confusion matrices, ROC curves, and decision boundaries update live."),
    ("⚖️", "Side-by-Side Comparison",
     "Train up to 3 models at once. Compare accuracy, F1-score, training time, and ROC curves on one dashboard."),
    ("🔮", "One-Click Predictions",
     "Enter feature values manually or upload a CSV batch. Download results with per-class confidence scores."),
    ("📤", "Bring Your Own Data",
     "Upload any CSV — auto-validates, detects column types, handles missing values, and encodes categoricals."),
    ("🧠", "Model Explainability",
     "Feature importance, permutation scores, and radar charts make model decisions easy to understand and present."),
]

f1, f2, f3 = st.columns(3)
for col, (icon, title, desc) in zip([f1, f2, f3], features[:3]):
    with col:
        st.markdown(
            f'<div class="feat-card">'
            f'<div class="feat-icon-box">{icon}</div>'
            f'<div class="feat-title">{title}</div>'
            f'<div class="feat-desc">{desc}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

st.markdown('<div style="height:0.75rem"></div>', unsafe_allow_html=True)

f4, f5, f6 = st.columns(3)
for col, (icon, title, desc) in zip([f4, f5, f6], features[3:]):
    with col:
        st.markdown(
            f'<div class="feat-card">'
            f'<div class="feat-icon-box">{icon}</div>'
            f'<div class="feat-title">{title}</div>'
            f'<div class="feat-desc">{desc}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

st.markdown('<div class="sec-divider"></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HOW IT WORKS  +  WHAT'S INCLUDED
# ══════════════════════════════════════════════════════════════════════════════
left_col, right_col = st.columns([1.3, 1])

with left_col:
    st.markdown(
        '<div class="sec-eyebrow">Workflow</div>'
        '<div class="sec-title">How It Works</div>'
        '<div class="sec-sub">Five steps from data to insight.</div>',
        unsafe_allow_html=True,
    )
    steps = [
        ("01", "Choose a Dataset",
         "Pick from 6 built-in datasets or upload your own CSV with automatic validation and preview."),
        ("02", "Configure & Train",
         "Select a model, tune hyperparameters with live sliders, and set train/test split and CV folds."),
        ("03", "Explore Visualizations",
         "Dive into confusion matrices, ROC curves, feature importance, learning curves, and decision boundaries."),
        ("04", "Compare Models",
         "Run up to 3 models side-by-side with radar charts, Pareto analysis, and automatic recommendations."),
        ("05", "Make Predictions",
         "Enter feature values or upload a batch CSV and download results with per-class confidence scores."),
    ]
    for num, title, desc in steps:
        st.markdown(
            f'<div class="step-card">'
            f'<div class="step-num">{num}</div>'
            f'<div><div class="step-title">{title}</div>'
            f'<div class="step-desc">{desc}</div></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

with right_col:
    st.markdown(
        '<div class="sec-eyebrow">Included</div>'
        '<div class="sec-title">What\'s Inside</div>'
        '<div class="sec-sub">Everything pre-configured and ready to use.</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="inc-card">', unsafe_allow_html=True)

    st.markdown('<div class="tag-lbl">Classification Models</div>', unsafe_allow_html=True)
    st.markdown(
        '<span class="tag">K-Nearest Neighbors</span>'
        '<span class="tag">Logistic Regression</span>'
        '<span class="tag">Decision Tree</span>'
        '<span class="tag">Random Forest</span>'
        '<span class="tag">Support Vector Machine</span>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="tag-lbl">Clustering</div>', unsafe_allow_html=True)
    st.markdown('<span class="tag">K-Means</span>', unsafe_allow_html=True)

    st.markdown('<div class="tag-lbl">Built-in Datasets</div>', unsafe_allow_html=True)
    st.markdown(
        '<span class="tag">Iris</span><span class="tag">Wine</span>'
        '<span class="tag">Breast Cancer</span><span class="tag">Digits</span>'
        '<span class="tag">Customer Segmentation</span><span class="tag">Iris Clustering</span>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="tag-lbl">Visualizations</div>', unsafe_allow_html=True)
    st.markdown(
        '<span class="tag">Confusion Matrix</span><span class="tag">ROC Curve</span>'
        '<span class="tag">Feature Importance</span><span class="tag">Learning Curve</span>'
        '<span class="tag">Decision Boundary</span><span class="tag">Cluster Plot</span>'
        '<span class="tag">Radar Chart</span><span class="tag">Elbow Plot</span>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="tag-lbl">Tech Stack</div>', unsafe_allow_html=True)
    st.markdown(
        '<span class="tag">Python 3.10</span><span class="tag">Streamlit 1.28</span>'
        '<span class="tag">scikit-learn 1.3</span><span class="tag">Plotly 5.17</span>'
        '<span class="tag">Pandas 2.1</span><span class="tag">NumPy 1.24</span>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# BOTTOM CTA
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="cta-band">
    <div class="cta-glow"></div>
    <div class="cta-eyebrow">Get Started Free</div>
    <div class="cta-title">Ready to Explore<br>Machine Learning?</div>
    <div class="cta-sub">No setup. No environment. No code.<br>Just load a dataset and start training in seconds.</div>
</div>
""", unsafe_allow_html=True)

_, cta_btn, _ = st.columns([2, 1, 2])
with cta_btn:
    if st.button("🚀 Start Now →", type="primary", use_container_width=True, key="bottom_cta"):
        st.switch_page("pages/1_📊_Dataset.py")

st.markdown(
    '<div style="text-align:center;margin-top:0.75rem;font-size:0.75rem;color:#374151;">'
    '100% free &nbsp;·&nbsp; No signup &nbsp;·&nbsp; Open source'
    '</div>',
    unsafe_allow_html=True,
)
st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    '<div class="footer-wrap">'
    '<div class="footer-left">'
    '<strong>ML Playground</strong> &nbsp;·&nbsp; '
    'Built by <strong>Radwan Rima</strong> &nbsp;·&nbsp; '
    'Streamlit · scikit-learn · Plotly'
    '</div>'
    '<a class="footer-link" href="https://github.com" target="_blank">⭐ Star on GitHub</a>'
    '</div>',
    unsafe_allow_html=True,
)
