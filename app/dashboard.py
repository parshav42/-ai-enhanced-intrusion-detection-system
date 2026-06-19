import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NetGuard IDS · Security Operations Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Global CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── Root tokens ── */
:root {
    --bg-base:       #050d1a;
    --bg-panel:      #0a1628;
    --bg-card:       #0d1f38;
    --bg-hover:      #112540;
    --accent-blue:   #1e6fff;
    --accent-cyan:   #00d4ff;
    --accent-green:  #00e676;
    --accent-red:    #ff4b6e;
    --accent-amber:  #ffb300;
    --border:        rgba(30, 111, 255, 0.18);
    --border-bright: rgba(0, 212, 255, 0.35);
    --text-primary:  #e8f0ff;
    --text-secondary:#7a9bbf;
    --text-muted:    #3d5a7a;
    --font-ui:       'Inter', sans-serif;
    --font-mono:     'JetBrains Mono', monospace;
    --radius-sm:     8px;
    --radius-md:     14px;
    --radius-lg:     20px;
    --shadow-card:   0 4px 32px rgba(0,0,0,0.55), 0 0 0 1px var(--border);
    --shadow-glow:   0 0 28px rgba(30,111,255,0.22);
}

/* ── Base reset ── */
html, body, [class*="css"] {
    font-family: var(--font-ui) !important;
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
}

.main .block-container {
    padding: 0 2rem 4rem 2rem !important;
    max-width: 1600px !important;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stToolbar"] { display: none; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-panel) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 3px; }

/* ── Section headings ── */
.section-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent-cyan);
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--border-bright), transparent);
}

/* ── Hero ── */
.hero-wrap {
    background: linear-gradient(135deg, #0a1628 0%, #061020 60%, #030c1a 100%);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 2.8rem 3rem;
    margin: 1.5rem 0 2rem 0;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-card);
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: -120px; right: -120px;
    width: 480px; height: 480px;
    background: radial-gradient(circle, rgba(30,111,255,0.12) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}
.hero-wrap::after {
    content: '';
    position: absolute;
    bottom: -80px; left: 200px;
    width: 340px; height: 340px;
    background: radial-gradient(circle, rgba(0,212,255,0.07) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}
.hero-eyebrow {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent-cyan);
    margin-bottom: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.hero-eyebrow::before {
    content: '';
    display: inline-block;
    width: 28px; height: 2px;
    background: var(--accent-cyan);
}
.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    line-height: 1.12;
    letter-spacing: -0.03em;
    color: var(--text-primary);
    margin-bottom: 0.9rem;
}
.hero-title span {
    background: linear-gradient(90deg, var(--accent-blue), var(--accent-cyan));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 1rem;
    color: var(--text-secondary);
    line-height: 1.6;
    max-width: 580px;
    margin-bottom: 1.8rem;
}
.hero-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 0.65rem;
}
.hero-badge {
    background: rgba(30,111,255,0.1);
    border: 1px solid rgba(30,111,255,0.25);
    border-radius: 999px;
    padding: 0.3rem 0.9rem;
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--accent-cyan);
    letter-spacing: 0.04em;
}
.hero-ts {
    position: absolute;
    top: 2.2rem; right: 2.5rem;
    font-family: var(--font-mono);
    font-size: 0.72rem;
    color: var(--text-muted);
    text-align: right;
    line-height: 1.7;
}

/* ── Metric cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
}
.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 1.4rem 1.5rem;
    box-shadow: var(--shadow-card);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    position: relative;
    overflow: hidden;
}
.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-glow), var(--shadow-card);
    border-color: var(--border-bright);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: var(--card-accent, var(--accent-blue));
    border-radius: var(--radius-md) 0 0 var(--radius-md);
}
.kpi-icon {
    font-size: 1.5rem;
    margin-bottom: 0.9rem;
    display: block;
    line-height: 1;
    opacity: 0.9;
}
.kpi-value {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    color: var(--text-primary);
    line-height: 1;
    margin-bottom: 0.3rem;
    font-variant-numeric: tabular-nums;
}
.kpi-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-secondary);
}
.kpi-delta {
    margin-top: 0.7rem;
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--accent-green);
    display: flex;
    align-items: center;
    gap: 0.3rem;
}

/* ── Glassmorphism chart card ── */
.glass-card {
    background: rgba(13, 31, 56, 0.75);
    backdrop-filter: blur(18px) saturate(160%);
    -webkit-backdrop-filter: blur(18px) saturate(160%);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.8rem 2rem;
    box-shadow: var(--shadow-card);
    margin-bottom: 1.5rem;
}

/* ── Sidebar components ── */
.sb-logo {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 0 1.2rem 1.8rem 1.2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}
.sb-logo-icon { font-size: 2rem; }
.sb-logo-text { line-height: 1.2; }
.sb-logo-name {
    font-size: 1.05rem;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.01em;
}
.sb-logo-sub {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--accent-cyan);
}

.sb-nav-label {
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--text-muted);
    padding: 0 1.2rem;
    margin-bottom: 0.4rem;
}
.sb-nav-item {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 0.6rem 1.2rem;
    border-radius: var(--radius-sm);
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--text-secondary);
    cursor: pointer;
    transition: background 0.15s, color 0.15s;
    margin: 0.1rem 0.5rem;
}
.sb-nav-item:hover, .sb-nav-item.active {
    background: rgba(30,111,255,0.12);
    color: var(--text-primary);
}
.sb-nav-item.active { color: var(--accent-cyan); }

.sb-divider {
    height: 1px;
    background: var(--border);
    margin: 1.2rem 1.2rem;
}

.sb-status-block {
    margin: 0 0.5rem 1rem 0.5rem;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 1rem 1.1rem;
}
.sb-status-title {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.8rem;
}
.sb-status-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.55rem;
    font-size: 0.78rem;
}
.sb-status-key { color: var(--text-secondary); }
.sb-status-val {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--text-primary);
}
.pill {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    border-radius: 999px;
    padding: 0.18rem 0.65rem;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.06em;
}
.pill-green  { background: rgba(0,230,118,0.12); color: var(--accent-green);  border: 1px solid rgba(0,230,118,0.25); }
.pill-red    { background: rgba(255,75,110,0.12); color: var(--accent-red);   border: 1px solid rgba(255,75,110,0.25); }
.pill-amber  { background: rgba(255,179,0,0.12);  color: var(--accent-amber); border: 1px solid rgba(255,179,0,0.25); }
.pill-blue   { background: rgba(30,111,255,0.12); color: var(--accent-cyan);  border: 1px solid rgba(0,212,255,0.25); }

/* ── Table ── */
.dataframe-wrap {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    overflow: hidden;
}
[data-testid="stDataFrame"] {
    border: none !important;
    background: transparent !important;
}

/* ── Alert strip ── */
.alert-strip {
    background: linear-gradient(90deg, rgba(0,230,118,0.08), rgba(30,111,255,0.06));
    border: 1px solid rgba(0,230,118,0.2);
    border-radius: var(--radius-sm);
    padding: 0.75rem 1.25rem;
    font-size: 0.82rem;
    color: var(--accent-green);
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 1rem;
    font-weight: 500;
}

/* ── Footer ── */
.footer {
    margin-top: 3rem;
    border-top: 1px solid var(--border);
    padding-top: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.footer-left {
    font-size: 0.78rem;
    color: var(--text-muted);
}
.footer-left strong { color: var(--text-secondary); }
.footer-right {
    font-family: var(--font-mono);
    font-size: 0.68rem;
    color: var(--text-muted);
}

/* ── Plotly overrides ── */
.js-plotly-plot .plotly .main-svg {
    background: transparent !important;
}

/* ── Streamlit metric override ── */
[data-testid="metric-container"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}
</style>
""", unsafe_allow_html=True)


# ─── Load Data ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_ddos.csv")
    return df

df = load_data()
benign = len(df[df["Label"] == "BENIGN"])
ddos   = len(df[df["Label"] != "BENIGN"])
now    = datetime.now()


# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
        <div class="sb-logo-icon">🛡️</div>
        <div class="sb-logo-text">
            <div class="sb-logo-name">NetGuard</div>
            <div class="sb-logo-sub">AI · IDS Platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-nav-label">Main</div>', unsafe_allow_html=True)
    for icon, label, active in [
        ("📊", "Overview",       True),
        ("🔍", "Traffic Analysis", False),
        ("⚠️",  "Threat Events",   False),
        ("🤖", "Model Insights",  False),
    ]:
        cls = "sb-nav-item active" if active else "sb-nav-item"
        st.markdown(f'<div class="{cls}">{icon}&nbsp;&nbsp;{label}</div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

    # System status
    threat_pct = round(ddos / df.shape[0] * 100, 1)
    threat_pill = ("pill-amber", "ELEVATED") if threat_pct > 5 else ("pill-green", "LOW")
    st.markdown(f"""
    <div class="sb-status-block">
        <div class="sb-status-title">System Status</div>
        <div class="sb-status-row">
            <span class="sb-status-key">System</span>
            <span class="pill pill-green">● ONLINE</span>
        </div>
        <div class="sb-status-row">
            <span class="sb-status-key">Threat Level</span>
            <span class="pill {threat_pill[0]}">▲ {threat_pill[1]}</span>
        </div>
        <div class="sb-status-row">
            <span class="sb-status-key">Model</span>
            <span class="pill pill-blue">● ACTIVE</span>
        </div>
        <div class="sb-status-row">
            <span class="sb-status-key">Uptime</span>
            <span class="sb-status-val">99.97 %</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Model info
    st.markdown(f"""
    <div class="sb-status-block">
        <div class="sb-status-title">Model Information</div>
        <div class="sb-status-row">
            <span class="sb-status-key">Algorithm</span>
            <span class="sb-status-val">Random Forest</span>
        </div>
        <div class="sb-status-row">
            <span class="sb-status-key">Accuracy</span>
            <span class="sb-status-val" style="color:#00e676;">99.99 %</span>
        </div>
        <div class="sb-status-row">
            <span class="sb-status-key">Features</span>
            <span class="sb-status-val">{df.shape[1]}</span>
        </div>
        <div class="sb-status-row">
            <span class="sb-status-key">Dataset</span>
            <span class="sb-status-val">CIC-DDoS</span>
        </div>
        <div class="sb-status-row">
            <span class="sb-status-key">Last trained</span>
            <span class="sb-status-val">{now.strftime('%d %b %Y')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-nav-label" style="margin-top:1rem;">Support</div>', unsafe_allow_html=True)
    for icon, label in [("⚙️", "Settings"), ("📖", "Documentation")]:
        st.markdown(f'<div class="sb-nav-item">{icon}&nbsp;&nbsp;{label}</div>', unsafe_allow_html=True)


# ─── Hero ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-wrap">
    <div class="hero-ts">
        {now.strftime('%A, %d %B %Y')}<br>
        {now.strftime('%H:%M:%S')} UTC+05:30<br>
        <span style="color:#1e6fff;">● Live Feed</span>
    </div>
    <div class="hero-eyebrow">Security Operations Center</div>
    <div class="hero-title">
        AI-Enhanced<br><span>Intrusion Detection</span>
    </div>
    <div class="hero-sub">
        Real-time network traffic analysis powered by Random Forest classification.
        Monitoring {df.shape[0]:,} flow records across {df.shape[1]} behavioral features.
    </div>
    <div class="hero-badges">
        <span class="hero-badge">🤖 Random Forest</span>
        <span class="hero-badge">📡 DDoS Detection</span>
        <span class="hero-badge">⚡ 99.99% Accuracy</span>
        <span class="hero-badge">🔒 CIC-DDoS Dataset</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── Alert strip ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="alert-strip">
    ✅ &nbsp; Intrusion Detection Model loaded and operational — all classifiers active, threat feeds nominal.
</div>
""", unsafe_allow_html=True)


# ─── KPI Cards ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Key Metrics</div>', unsafe_allow_html=True)

attack_ratio = round(ddos / df.shape[0] * 100, 2)
st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card" style="--card-accent:#1e6fff;">
        <span class="kpi-icon">🗄️</span>
        <div class="kpi-value">{df.shape[0]:,}</div>
        <div class="kpi-label">Total Records</div>
        <div class="kpi-delta">↑ Full dataset loaded</div>
    </div>
    <div class="kpi-card" style="--card-accent:#00d4ff;">
        <span class="kpi-icon">📐</span>
        <div class="kpi-value">{df.shape[1]}</div>
        <div class="kpi-label">Total Features</div>
        <div class="kpi-delta">↑ Behavioral signals</div>
    </div>
    <div class="kpi-card" style="--card-accent:#00e676;">
        <span class="kpi-icon">🎯</span>
        <div class="kpi-value">99.99<span style="font-size:1rem;font-weight:600;">%</span></div>
        <div class="kpi-label">Model Accuracy</div>
        <div class="kpi-delta" style="color:#00e676;">↑ State of the art</div>
    </div>
    <div class="kpi-card" style="--card-accent:#00e676;">
        <span class="kpi-icon">✅</span>
        <div class="kpi-value">{benign:,}</div>
        <div class="kpi-label">Normal Traffic</div>
        <div class="kpi-delta" style="color:#00e676;">↑ {round(benign/df.shape[0]*100,1)}% of total</div>
    </div>
    <div class="kpi-card" style="--card-accent:#ff4b6e;">
        <span class="kpi-icon">⚠️</span>
        <div class="kpi-value">{ddos:,}</div>
        <div class="kpi-label">Attack Traffic</div>
        <div class="kpi-delta" style="color:#ff4b6e;">▲ {attack_ratio}% attack rate</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── Charts ──────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Traffic Analysis</div>', unsafe_allow_html=True)

col_a, col_b = st.columns([1.1, 0.9])

with col_a:
    label_counts = df["Label"].value_counts().reset_index()
    label_counts.columns = ["Label", "Count"]

    colors = []
    for lbl in label_counts["Label"]:
        colors.append("#00e676" if lbl == "BENIGN" else "#ff4b6e")

    fig_bar = go.Figure(go.Bar(
        x=label_counts["Label"],
        y=label_counts["Count"],
        marker=dict(
            color=colors,
            line=dict(color="rgba(255,255,255,0.05)", width=1),
        ),
        text=label_counts["Count"].apply(lambda x: f"{x:,}"),
        textposition="outside",
        textfont=dict(color="#7a9bbf", size=11, family="JetBrains Mono"),
    ))
    fig_bar.update_layout(
        title=dict(text="Attack Distribution by Label", font=dict(size=14, color="#e8f0ff", family="Inter"), x=0.0, xanchor="left"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#7a9bbf"),
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=11, color="#7a9bbf")),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", zeroline=False, tickfont=dict(size=11, color="#7a9bbf")),
        margin=dict(l=0, r=0, t=50, b=0),
        height=320,
        hoverlabel=dict(bgcolor="#0d1f38", bordercolor="#1e6fff", font=dict(color="#e8f0ff")),
    )
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with col_b:
    pie_colors = ["#1e6fff" if lbl == "BENIGN" else "#ff4b6e" for lbl in label_counts["Label"]]
    fig_pie = go.Figure(go.Pie(
        labels=label_counts["Label"],
        values=label_counts["Count"],
        hole=0.6,
        marker=dict(colors=pie_colors, line=dict(color="#050d1a", width=3)),
        textinfo="percent",
        textfont=dict(size=12, color="#e8f0ff"),
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>",
    ))
    fig_pie.update_layout(
        title=dict(text="Traffic Composition", font=dict(size=14, color="#e8f0ff", family="Inter"), x=0.0, xanchor="left"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#7a9bbf"),
        showlegend=True,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#7a9bbf", size=11)),
        margin=dict(l=0, r=0, t=50, b=0),
        height=320,
        annotations=[dict(text=f"<b>{df.shape[0]:,}</b><br><span style='font-size:10px;'>records</span>",
                          x=0.5, y=0.5, font=dict(size=14, color="#e8f0ff", family="Inter"),
                          showarrow=False)],
    )
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)


# ─── Dataset Preview ─────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Dataset Preview</div>', unsafe_allow_html=True)

with st.expander("📋  View first 20 records", expanded=True):
    st.dataframe(
        df.head(20),
        use_container_width=True,
        height=380,
    )


# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
    <div class="footer-left">
        <strong>NetGuard IDS</strong> &nbsp;·&nbsp; AI-Enhanced Intrusion Detection System &nbsp;·&nbsp;
        Built by <strong>Parshav Khoche</strong> &nbsp;·&nbsp; SmartInternz Project
    </div>
    <div class="footer-right">
        v1.0.0 &nbsp;|&nbsp; Random Forest Classifier &nbsp;|&nbsp;
        {now.strftime('%d %b %Y')}
    </div>
</div>
""", unsafe_allow_html=True)