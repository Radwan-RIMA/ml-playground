"""Shared CSS injected on every page via inject_global_css()."""
import streamlit as st


GLOBAL_CSS = """
<style>
/* ── Google Font ─────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Hide default Streamlit chrome ────────────────────────────────────── */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }

/* ── Page background ──────────────────────────────────────────────────── */
.stApp {
    background: #080B14;
}

/* ── Sidebar ─────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #111827 100%);
    border-right: 1px solid rgba(255,75,75,0.15);
}
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #FF4B4B;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}

/* ── Sidebar nav links ───────────────────────────────────────────────── */
[data-testid="stSidebarNav"] { padding-top: 0; }
[data-testid="stSidebarNavItems"] { padding: 0 0.5rem 1rem; }
[data-testid="stSidebarNavLink"] {
    border-radius: 10px;
    padding: 0.55rem 0.85rem;
    margin: 3px 0;
    color: #555 !important;
    font-size: 0.875rem;
    font-weight: 500;
    transition: all 0.15s ease;
    border: 1px solid transparent;
}
[data-testid="stSidebarNavLink"]:hover {
    background: rgba(255,75,75,0.08) !important;
    color: #FF4B4B !important;
    border-color: rgba(255,75,75,0.18);
    padding-left: 1.1rem;
}
[data-testid="stSidebarNavLink"][aria-current="page"] {
    background: rgba(255,75,75,0.1) !important;
    color: #FF4B4B !important;
    font-weight: 700;
    border-left: 3px solid #FF4B4B;
    border-color: rgba(255,75,75,0.25);
}
[data-testid="stSidebarNavSeparator"] { display: none; }

/* ── Buttons ─────────────────────────────────────────────────────────── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #FF4B4B, #ff6b35);
    border: none;
    border-radius: 10px;
    color: white;
    font-weight: 700;
    letter-spacing: 0.03em;
    padding: 0.65rem 1.5rem;
    transition: all 0.25s ease;
    box-shadow: 0 4px 20px rgba(255,75,75,0.35);
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(255,75,75,0.55);
    background: linear-gradient(135deg, #ff3333, #ff5500);
}
.stButton > button:not([kind="primary"]) {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 10px;
    color: #e0e0e0;
    font-weight: 500;
    transition: all 0.2s ease;
}
.stButton > button:not([kind="primary"]):hover {
    background: rgba(255,75,75,0.1);
    border-color: rgba(255,75,75,0.4);
    color: #FF4B4B;
}

/* ── Selectbox / Radio ───────────────────────────────────────────────── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px;
}
.stRadio > div { gap: 0.5rem; }

/* ── Sliders ─────────────────────────────────────────────────────────── */
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
    background: #FF4B4B;
    box-shadow: 0 0 10px rgba(255,75,75,0.6);
}

/* ── Tabs ────────────────────────────────────────────────────────────── */
[data-testid="stTabs"] button {
    font-weight: 600;
    color: #888;
    border-bottom: 2px solid transparent;
    transition: all 0.2s;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #FF4B4B;
    border-bottom: 2px solid #FF4B4B;
}

/* ── Metric cards (native st.metric) ─────────────────────────────────── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(255,75,75,0.08), rgba(255,107,53,0.04));
    border: 1px solid rgba(255,75,75,0.2);
    border-radius: 14px;
    padding: 1rem 1.25rem;
    transition: box-shadow 0.2s;
}
[data-testid="stMetric"]:hover {
    box-shadow: 0 0 20px rgba(255,75,75,0.15);
}
[data-testid="stMetricLabel"] { color: #888 !important; font-size: 0.78rem !important; }
[data-testid="stMetricValue"] { color: #FAFAFA !important; font-weight: 700 !important; }

/* ── DataFrames ──────────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    overflow: hidden;
}

/* ── Expanders ───────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
}

/* ── Alerts ──────────────────────────────────────────────────────────── */
[data-testid="stAlert"][data-type="info"] {
    background: rgba(0,180,216,0.08);
    border: 1px solid rgba(0,180,216,0.25);
    border-radius: 10px;
}
[data-testid="stAlert"][data-type="success"] {
    background: rgba(0,200,130,0.08);
    border: 1px solid rgba(0,200,130,0.25);
    border-radius: 10px;
}
[data-testid="stAlert"][data-type="warning"] {
    background: rgba(255,165,0,0.08);
    border: 1px solid rgba(255,165,0,0.25);
    border-radius: 10px;
}

/* ── Divider ─────────────────────────────────────────────────────────── */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,75,75,0.3), transparent);
    margin: 2rem 0;
}

/* ── Scrollbar ───────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #FF4B4B44; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #FF4B4B99; }

/* ── Reusable utility classes ─────────────────────────────────────────── */

.gradient-text {
    background: linear-gradient(135deg, #FF4B4B 0%, #FF8C42 50%, #FFD166 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.glass-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.5rem;
    transition: all 0.25s ease;
}
.glass-card:hover {
    border-color: rgba(255,75,75,0.3);
    box-shadow: 0 8px 32px rgba(255,75,75,0.1);
    transform: translateY(-2px);
}

.accent-card {
    background: linear-gradient(135deg, rgba(255,75,75,0.12), rgba(255,107,53,0.06));
    border: 1px solid rgba(255,75,75,0.25);
    border-radius: 16px;
    padding: 1.5rem;
}

.metric-card {
    background: linear-gradient(135deg, rgba(20,24,40,1), rgba(30,35,55,1));
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.25s ease;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #FF4B4B, #FF8C42);
}
.metric-card:hover {
    border-color: rgba(255,75,75,0.3);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    transform: translateY(-3px);
}
.metric-value {
    font-size: 2.2rem;
    font-weight: 800;
    color: #FAFAFA;
    line-height: 1.1;
}
.metric-label {
    font-size: 0.78rem;
    font-weight: 500;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.35rem;
}
.metric-bar-wrap {
    height: 4px;
    background: rgba(255,255,255,0.06);
    border-radius: 2px;
    margin-top: 0.75rem;
    overflow: hidden;
}
.metric-bar {
    height: 100%;
    border-radius: 2px;
    background: linear-gradient(90deg, #FF4B4B, #FF8C42);
    transition: width 0.8s ease;
}

.page-header {
    margin-bottom: 2rem;
}
.page-title {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #FAFAFA, #adb5bd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.25rem 0;
}
.page-subtitle {
    color: #555;
    font-size: 1rem;
    font-weight: 400;
    margin: 0;
}

.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #FAFAFA;
    letter-spacing: 0.02em;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(255,75,75,0.3), transparent);
    margin-left: 0.5rem;
}

.badge-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: rgba(255,75,75,0.1);
    border: 1px solid rgba(255,75,75,0.25);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.82rem;
    font-weight: 600;
    color: #FF4B4B;
    margin: 3px;
}

.badge-pill-gray {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.82rem;
    font-weight: 500;
    color: #adb5bd;
    margin: 3px;
}

.timeline-step {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 1rem 0;
    border-left: 2px solid rgba(255,75,75,0.15);
    padding-left: 1.5rem;
    margin-left: 1rem;
    position: relative;
}
.timeline-step::before {
    content: '';
    width: 12px; height: 12px;
    border-radius: 50%;
    background: #FF4B4B;
    box-shadow: 0 0 12px #FF4B4B;
    position: absolute;
    left: -7px; top: 1.2rem;
    flex-shrink: 0;
}
.timeline-num {
    color: #FF4B4B;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.timeline-title {
    color: #FAFAFA;
    font-size: 1rem;
    font-weight: 700;
    margin: 0.15rem 0;
}
.timeline-desc {
    color: #666;
    font-size: 0.88rem;
}

.stat-number-xl {
    font-size: 3rem;
    font-weight: 900;
    background: linear-gradient(135deg, #FF4B4B, #FF8C42);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}
.stat-label {
    font-size: 0.8rem;
    color: #555;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.4rem;
}

.glow-divider {
    width: 60px;
    height: 3px;
    background: linear-gradient(90deg, #FF4B4B, #FF8C42);
    border-radius: 2px;
    margin: 0.75rem 0 1.25rem;
    box-shadow: 0 0 12px rgba(255,75,75,0.5);
}

.model-selector-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1.25rem;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: center;
}
.model-selector-card:hover,
.model-selector-card.active {
    background: rgba(255,75,75,0.08);
    border-color: rgba(255,75,75,0.35);
    box-shadow: 0 4px 20px rgba(255,75,75,0.12);
}

.result-badge {
    display: inline-block;
    padding: 6px 18px;
    border-radius: 30px;
    font-weight: 800;
    font-size: 1.1rem;
    letter-spacing: 0.02em;
}
.result-badge-green {
    background: rgba(0,200,130,0.15);
    border: 1px solid rgba(0,200,130,0.4);
    color: #00C882;
}
.result-badge-yellow {
    background: rgba(255,180,0,0.12);
    border: 1px solid rgba(255,180,0,0.4);
    color: #FFB400;
}
.result-badge-red {
    background: rgba(255,75,75,0.12);
    border: 1px solid rgba(255,75,75,0.35);
    color: #FF4B4B;
}

.sidebar-nav-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.6rem 0.75rem;
    border-radius: 10px;
    margin-bottom: 0.25rem;
    color: #666;
    font-size: 0.9rem;
    font-weight: 500;
    transition: all 0.15s;
    cursor: pointer;
}
.sidebar-nav-item.active {
    background: rgba(255,75,75,0.12);
    color: #FF4B4B;
    font-weight: 700;
}
</style>
"""


def inject_global_css():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def metric_card(value: str, label: str, pct: float = None, icon: str = ""):
    """Render a styled metric card with optional progress bar."""
    bar_html = ""
    if pct is not None:
        bar_html = f"""
        <div class="metric-bar-wrap">
            <div class="metric-bar" style="width:{min(pct,100):.1f}%"></div>
        </div>"""
    return f"""
    <div class="metric-card">
        <div style="font-size:1.5rem;margin-bottom:0.3rem">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {bar_html}
    </div>"""


def page_header(title: str, subtitle: str = "", icon: str = ""):
    st.markdown(f"""
    <div class="page-header">
        <div style="display:flex;align-items:center;gap:0.75rem">
            <span style="font-size:1.8rem">{icon}</span>
            <div>
                <div class="page-title">{title}</div>
                {'<div class="page-subtitle">' + subtitle + '</div>' if subtitle else ''}
            </div>
        </div>
        <div class="glow-divider"></div>
    </div>
    """, unsafe_allow_html=True)


def section_title(text: str):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


def glass_card(content_html: str):
    st.markdown(f'<div class="glass-card">{content_html}</div>', unsafe_allow_html=True)


def render_sidebar_status():
    """Show branding + dataset/model status in sidebar."""
    import streamlit as st
    with st.sidebar:
        st.markdown(
            '<div style="padding:1.25rem 1rem 0.75rem;">'
            '<div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.5rem;">'
            '<div style="width:34px;height:34px;border-radius:10px;flex-shrink:0;'
            'background:linear-gradient(135deg,#FF4B4B,#FF8C42);'
            'display:flex;align-items:center;justify-content:center;font-size:1rem;">🤖</div>'
            '<div>'
            '<div style="font-size:0.9rem;font-weight:800;color:#FAFAFA;line-height:1.1;">ML Playground</div>'
            '<div style="font-size:0.68rem;color:#555;font-weight:500;">Interactive ML Explorer</div>'
            '</div></div>'
            '<div style="height:1px;background:linear-gradient(90deg,rgba(255,75,75,0.3),transparent);margin:0.5rem 0;"></div>'
            '<div style="font-size:0.6rem;font-weight:700;color:#FF4B4B;text-transform:uppercase;'
            'letter-spacing:0.12em;margin-bottom:0.35rem;">Navigation</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown("---")
        st.markdown("### Session Status")
        df = st.session_state.get("df")
        dataset_name = st.session_state.get("dataset_name", "—")
        task = st.session_state.get("task", "—")
        results = st.session_state.get("training_results", {})

        if df is not None:
            st.markdown(f"""
            <div style="background:rgba(0,200,130,0.08);border:1px solid rgba(0,200,130,0.2);
                        border-radius:10px;padding:0.75rem 1rem;margin-bottom:0.5rem">
                <div style="color:#00C882;font-size:0.72rem;font-weight:700;text-transform:uppercase;
                            letter-spacing:0.08em">Dataset</div>
                <div style="color:#FAFAFA;font-size:0.9rem;font-weight:600;margin-top:0.2rem">{dataset_name}</div>
                <div style="color:#555;font-size:0.78rem">{df.shape[0]} rows · {df.shape[1]} cols · {task}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
                        border-radius:10px;padding:0.75rem 1rem;margin-bottom:0.5rem">
                <div style="color:#555;font-size:0.85rem">No dataset loaded</div>
            </div>
            """, unsafe_allow_html=True)

        if results:
            st.markdown(f"""
            <div style="background:rgba(255,75,75,0.08);border:1px solid rgba(255,75,75,0.2);
                        border-radius:10px;padding:0.75rem 1rem">
                <div style="color:#FF4B4B;font-size:0.72rem;font-weight:700;text-transform:uppercase;
                            letter-spacing:0.08em">Trained Models</div>
                <div style="color:#FAFAFA;font-size:0.88rem;margin-top:0.3rem">
                    {'<br>'.join(f'• {m}' for m in results)}
                </div>
            </div>
            """, unsafe_allow_html=True)
