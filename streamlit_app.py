import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
import random
import io
import html

st.set_page_config(page_title="The Night Desk", page_icon="📰", layout="wide", initial_sidebar_state="collapsed")

API_URL = "https://nc-rzir.onrender.com"

def esc(val):
    if val is None:
        return ""
    return html.escape(str(val))

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Anton&family=IBM+Plex+Mono:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Sans:ital,wght@0,400;0,600;0,700;1,400&family=Playfair+Display:ital,wght@0,600;0,700;0,900;1,600;1,700&display=swap');

:root {
    --bg: #14161C;
    --bg-raised: #1D2028;
    --bg-inset: #191B21;
    --text: #EDE8DE;
    --text-soft: #9B968C;
    --rule: #33363F;
    --wine: #B23A48;
    --emerald: #2F6B55;
    --brass: #C9A227;
}

/* Background grain overlay */
body::before {
    content: "";
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    opacity: 0.035;
    pointer-events: none;
    z-index: 99999;
    background: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
}

/* Hide Streamlit Chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Base typography overrides */
html, body, [class*="css"]  {
    font-family: 'IBM Plex Sans', sans-serif;
    color: var(--text);
    background-color: var(--bg);
}

/* Masthead */
.masthead-title {
    font-family: 'Playfair Display', serif;
    font-size: 54px;
    font-weight: 900;
    letter-spacing: 0.03em;
    color: var(--brass);
    background: linear-gradient(135deg, #C9A227 0%, #EDE8DE 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
    line-height: 1.05;
}
.masthead-subtitle {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    text-transform: uppercase;
    color: var(--text-soft);
    letter-spacing: 0.08em;
    margin-top: 6px;
    margin-bottom: 12px;
}
.masthead-rule {
    border-top: 1px dotted var(--rule);
    border-bottom: 3px double var(--brass);
    height: 6px;
    margin-bottom: 20px;
    opacity: 0.85;
}
.wire-status {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    font-weight: 600;
}

/* Top Masthead Navigation Bar */
.nav-group-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    text-transform: uppercase;
    color: var(--brass);
    letter-spacing: 0.12em;
    font-weight: 600;
    margin-bottom: 6px;
}

/* Drop Cap */
.drop-cap::first-letter {
    font-family: 'Playfair Display', serif;
    font-size: 46px;
    float: left;
    line-height: 0.8;
    padding-top: 4px;
    padding-right: 8px;
    padding-bottom: 2px;
    color: var(--brass);
    font-weight: 700;
}

/* Headers */
h1, h2, h3 {
    font-family: 'Playfair Display', serif;
    letter-spacing: 0.03em;
    color: var(--text);
}
h1 { font-size: 32px !important; }
h2 { font-size: 24px !important; margin-top: 1.2rem !important; margin-bottom: 0.8rem !important; font-weight: 600 !important; }

/* Buttons */
.stButton>button {
    border-radius: 2px !important;
    border: 1px solid var(--rule) !important;
    color: var(--text) !important;
    background-color: var(--bg-inset) !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    font-weight: 600 !important;
    transition: all 0.2s ease-in-out !important;
}
.stButton>button:hover {
    background-color: var(--wine) !important;
    border-color: var(--wine) !important;
    color: #EDE8DE !important;
}

/* Inputs */
.stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div, .stNumberInput>div>div>input {
    border-radius: 2px !important;
    border: 1px solid var(--rule) !important;
    background-color: var(--bg-inset) !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    color: var(--text) !important;
}
.stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus, .stSelectbox>div>div>div:focus-within {
    border-color: var(--wine) !important;
    box-shadow: 0 0 0 1px var(--wine) !important;
}

/* Custom Components */
.stat-card {
    background-color: var(--bg-raised);
    border: 1px solid var(--rule);
    padding: 15px;
    border-radius: 2px;
}
.stat-card-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    text-transform: uppercase;
    color: var(--text-soft);
    margin-bottom: 5px;
}
.stat-card-value {
    font-family: 'Playfair Display', serif;
    font-size: 36px;
    font-weight: 700;
    color: var(--text);
    line-height: 1.1;
}

.dispatch-note {
    background-color: var(--bg-raised);
    padding: 12px 16px;
    border-radius: 2px;
    margin-bottom: 1.2rem;
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 14px;
}
.dispatch-note-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 4px;
    display: block;
    letter-spacing: 0.08em;
}
.dispatch-success { border-left: 4px solid var(--emerald); }
.dispatch-error { border-left: 4px solid var(--wine); }
.dispatch-info { border-left: 4px solid var(--brass); }
.dispatch-success .dispatch-note-label { color: var(--emerald); }
.dispatch-error .dispatch-note-label { color: var(--wine); }
.dispatch-info .dispatch-note-label { color: var(--brass); }

/* Wax Seal Badge */
.wax-seal {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background-color: var(--wine);
    color: var(--brass);
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 15px;
    padding: 10px 16px;
    border-radius: 48% 52% 49% 51% / 51% 48% 52% 49%;
    border: 2px solid var(--brass);
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.6), 0 4px 10px rgba(0,0,0,0.6);
    filter: drop-shadow(0 4px 6px rgba(0,0,0,0.5));
    transform: rotate(-3deg);
    letter-spacing: 0.06em;
    text-align: center;
    line-height: 1.2;
}

.stamp-container {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    margin: 8px 0;
}
.stamp-conf {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: var(--brass);
    margin-top: 6px;
    letter-spacing: 0.05em;
    opacity: 0.9;
}

/* Headline-Style Prediction Result (File a Story) */
.headline-result-box {
    border-left: 4px solid var(--wine);
    padding-left: 20px;
    margin: 15px 0 25px 0;
}
.headline-result-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    text-transform: uppercase;
    color: var(--brass);
    letter-spacing: 0.1em;
    margin-bottom: 4px;
}
.headline-result-category {
    font-family: 'Playfair Display', serif;
    font-size: 46px;
    font-weight: 900;
    color: var(--text);
    line-height: 1.1;
    text-transform: uppercase;
}

/* Editorial Chart Caption */
.chart-caption {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: var(--text-soft);
    margin-top: 6px;
    border-top: 1px dotted var(--rule);
    padding-top: 6px;
}

/* Unboxed Metric Displays */
.hero-metric-num {
    font-family: 'Playfair Display', serif;
    font-size: 56px;
    font-weight: 900;
    color: var(--brass);
    line-height: 1;
}
.hero-metric-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    text-transform: uppercase;
    color: var(--text-soft);
    letter-spacing: 0.08em;
    margin-top: 4px;
}
.metric-inline-group {
    display: flex;
    gap: 20px;
    align-items: center;
    border-top: 1px dotted var(--rule);
    border-bottom: 1px dotted var(--rule);
    padding: 12px 0;
    margin: 15px 0;
}
.metric-inline-item {
    display: flex;
    flex-direction: column;
}
.metric-inline-val {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 18px;
    font-weight: 600;
    color: var(--text);
}
.metric-inline-lbl {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 11px;
    text-transform: uppercase;
    color: var(--text-soft);
}

/* Archive Entry */
.archive-entry {
    border-left: 2px solid var(--rule);
    padding-left: 15px;
    margin-bottom: 20px;
    transition: border-color 0.2s ease;
}
.archive-entry:hover {
    border-left-color: var(--brass);
}
.archive-title {
    font-family: 'IBM Plex Sans', sans-serif;
    font-weight: 700;
    font-size: 17px;
    color: var(--text);
    margin-bottom: 4px;
}
.archive-snippet {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 14px;
    color: var(--text-soft);
    line-height: 1.4;
}

/* Telegram Slip */
.telegram-slip {
    background-color: var(--bg-raised);
    border: 1px solid var(--rule);
    padding: 18px;
    border-radius: 2px;
    height: 100%;
    transition: transform 0.2s ease-out, box-shadow 0.2s ease-out;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
.telegram-slip:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(0,0,0,0.5);
}
.slip-reporter {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: var(--text-soft);
    text-transform: uppercase;
    margin-bottom: 12px;
    border-bottom: 1px dotted var(--rule);
    padding-bottom: 5px;
}
.slip-agreement {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 14px;
    font-weight: 600;
    margin-top: 12px;
    text-align: center;
}
.agree-yes { color: var(--emerald); }
.agree-no { color: var(--wine); }

/* Notebook Box */
.notebook-box {
    background-color: var(--bg-inset);
    border: 1px dashed var(--rule);
    padding: 16px 20px;
    border-radius: 2px;
    margin: 15px 0;
}

/* Pull Quote */
.pull-quote {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 19px;
    border-left: 4px solid var(--brass);
    padding-left: 15px;
    margin: 15px 0;
    color: var(--text);
    line-height: 1.4;
}

/* Dataframe/Table overrides */
.stTable, .dataframe {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 14px;
    color: var(--text);
}
.stTable th {
    font-family: 'IBM Plex Sans', sans-serif !important;
    color: var(--text-soft) !important;
    border-bottom: 1px solid var(--rule) !important;
    text-transform: uppercase;
    font-size: 12px;
}
.stTable td {
    border-bottom: 1px solid var(--rule) !important;
}

/* Leaderboard Rank */
.lb-rank {
    font-family: 'Playfair Display', serif;
    font-size: 32px;
    color: var(--brass);
    opacity: 0.85;
}

/* Animation */
.reveal {
    animation: fadeSlideUp 0.3s ease-out forwards;
}
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

@media (prefers-reduced-motion: reduce) {
    .reveal { animation: none; opacity: 1; transform: none; }
    .telegram-slip:hover { transform: none; box-shadow: none; }
}

.annotations-list {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    color: var(--text);
    margin-bottom: 4px;
}

.mono-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    border: 1px solid var(--text-soft);
    color: var(--text-soft);
    padding: 2px 6px;
    border-radius: 2px;
    text-transform: uppercase;
    background: var(--bg-inset);
}
</style>
""", unsafe_allow_html=True)

colors = ['#B23A48', '#2F6B55', '#C9A227', '#EDE8DE', '#9B968C', '#5B5F68', '#4A7A7B', '#8A4F3D']
pio.templates["wireroom"] = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor='#1D2028',
        plot_bgcolor='#1D2028',
        font=dict(family='IBM Plex Sans, sans-serif', color='#EDE8DE'),
        colorway=colors,
        xaxis=dict(gridcolor='#33363F', zerolinecolor='#33363F'),
        yaxis=dict(gridcolor='#33363F', zerolinecolor='#33363F'),
    )
)
pio.templates.default = "wireroom"

def dispatch_note(msg_type, msg):
    type_class = f"dispatch-{esc(msg_type).lower()}"
    label = "DISPATCH" if str(msg_type).lower() == 'success' else str(msg_type).upper()
    st.markdown(f"""
    <div class="dispatch-note {type_class}">
        <span class="dispatch-note-label">{esc(label)}</span>
        {msg}
    </div>
    """, unsafe_allow_html=True)

def render_stamp(category: str, confidence: float | None = None) -> str:
    conf_html = f'<span class="stamp-conf">{confidence*100:.1f}% CONFIDENCE</span>' if confidence is not None else ''
    return f"""
    <div class="stamp-container">
        <div class="wax-seal">{esc(category)}</div>
        {conf_html}
    </div>
    """

@st.cache_data(ttl=60)
def fetch_models():
    try:
        res = requests.get(f"{API_URL}/models")
        if res.status_code == 200:
            return res.json()
    except:
        pass
    return []

@st.cache_data(ttl=60)
def fetch_model_details(model_id):
    try:
        res = requests.get(f"{API_URL}/models/{model_id}")
        if res.status_code == 200:
            return res.json()
    except:
        pass
    return None

@st.cache_data(ttl=60)
def fetch_leaderboard():
    try:
        res = requests.get(f"{API_URL}/leaderboard")
        if res.status_code == 200:
            return res.json()
    except:
        pass
    return []

def predict(text, model_id):
    try:
        res = requests.post(f"{API_URL}/predict", json={"text": text, "model_id": model_id})
        if res.status_code == 200:
            return res.json()
    except:
        pass
    return None

def predict_compare(text):
    try:
        res = requests.post(f"{API_URL}/predict/compare", json={"text": text})
        if res.status_code == 200:
            return res.json()
    except:
        pass
    return None

@st.cache_data
def load_archive_sample():
    try:
        df = pd.read_csv("news_data.csv")
        if 'category' not in df.columns:
            return pd.DataFrame()
        sampled = df.groupby('category').apply(lambda x: x.sample(min(len(x), 100), random_state=42)).reset_index(drop=True)
        return sampled
    except Exception as e:
        return pd.DataFrame()

archive_df = load_archive_sample()

if 'challenge_wins' not in st.session_state:
    st.session_state.challenge_wins = 0
if 'challenge_played' not in st.session_state:
    st.session_state.challenge_played = 0
if 'current_challenge' not in st.session_state:
    st.session_state.current_challenge = None
if 'challenge_revealed' not in st.session_state:
    st.session_state.challenge_revealed = False
if 'challenge_guess' not in st.session_state:
    st.session_state.challenge_guess = None

if 'current_page' not in st.session_state:
    st.session_state.current_page = "File a Story"

models = fetch_models()
wire_status_html = "<span class='wire-status' style='color: var(--emerald);'>● WIRE ACTIVE</span>" if models else "<span class='wire-status' style='color: var(--wine);'>● DESK OFFLINE</span>"

st.markdown(f"""
<div style="display: flex; justify-content: space-between; align-items: flex-end;">
    <div>
        <h1 class="masthead-title">THE NIGHT DESK</h1>
        <div class="masthead-subtitle">AN EDITORIAL DESK FOR MACHINE LEARNING · 6 CORRESPONDENTS ON DUTY</div>
    </div>
    <div style="padding-bottom: 12px;">{wire_status_html}</div>
</div>
<div class="masthead-rule"></div>
""", unsafe_allow_html=True)

if not models:
    dispatch_note("error", f"Cannot connect to backend server on {esc(API_URL)}. Ensure uvicorn is running.")
    st.stop()

current = st.session_state.current_page

st.markdown("<div class='nav-group-title'>THE DESK</div>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
desk_pages = ["File a Story", "Correspondent Profiles", "Standings", "All Hands on Deck"]
for p, col in zip(desk_pages, [c1, c2, c3, c4]):
    is_active = (p == current)
    label = f"▸ {p}" if is_active else p
    if col.button(label, key=f"nav_{p}", use_container_width=True):
        st.session_state.current_page = p
        st.rerun()

st.markdown("<div class='nav-group-title' style='margin-top: 10px;'>THE ARCHIVE</div>", unsafe_allow_html=True)
a1, a2, a3, a4 = st.columns(4)
archive_pages = ["Batch Wire", "The Morgue", "Editor's Challenge", "Head-to-Head"]
for p, col in zip(archive_pages, [a1, a2, a3, a4]):
    is_active = (p == current)
    label = f"▸ {p}" if is_active else p
    if col.button(label, key=f"nav_{p}", use_container_width=True):
        st.session_state.current_page = p
        st.rerun()

st.markdown("<div style='border-bottom: 1px dotted var(--rule); margin: 15px 0 25px 0;'></div>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h3 style='margin-top:0;'>DESK SUMMARY</h3>", unsafe_allow_html=True)
    st.markdown(f"<div class='annotations-list'>Active Page: <b>{esc(current)}</b></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='annotations-list'>Loaded Models: {len(models)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='annotations-list'>Backend: {esc(API_URL)}</div>", unsafe_allow_html=True)

model_options = {m['display_name']: m['model_id'] for m in models}
default_model_name = next((m['display_name'] for m in models if m['model_id'] == 'logistic_regression'), list(model_options.keys())[0])

selected_page = st.session_state.current_page

if selected_page == "File a Story":
    st.markdown("<h2>File a story to the desk</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        text_input = st.text_area("News Text", height=140, label_visibility="collapsed", placeholder="Enter a headline or story dispatch to be classified...")
    with col2:
        selected_name = st.selectbox("Assign to Correspondent", options=list(model_options.keys()), index=list(model_options.keys()).index(default_model_name), label_visibility="collapsed")
        predict_btn = st.button("File Dispatch", use_container_width=True)
        
    if predict_btn:
        if not text_input.strip():
            dispatch_note("info", "Please enter a story dispatch before filing.")
        else:
            with st.spinner("Processing dispatch..."):
                result = predict(text_input, model_options[selected_name])
                if result:
                    st.markdown("<div class='reveal'>", unsafe_allow_html=True)
                    dispatch_note("success", f"Dispatch categorized by {esc(selected_name)}.")
                    
                    c1, c2 = st.columns([3, 2])
                    with c1:
                        cat_str = esc(result['predicted_category'])
                        conf_val = result['confidence']
                        
                        st.markdown(f"""
                        <div class="headline-result-box">
                            <div class="headline-result-label">VERDICT DISPATCH</div>
                            <div style="display:flex; align-items:center; gap:20px; flex-wrap:wrap;">
                                <div class="headline-result-category">{cat_str}</div>
                                {render_stamp(cat_str, conf_val)}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        is_linear = model_options[selected_name] in ['logistic_regression', 'naive_bayes', 'linear_svm']
                        expander_title = "EXACT WORD WEIGHTS IN DISPATCH" if is_linear else "TYPICAL CATEGORY WORDS"
                        
                        st.markdown(f"<div style='margin-top:15px;'><div class='stat-card-label'>{expander_title}</div>", unsafe_allow_html=True)
                        if not is_linear:
                            st.markdown("<div style='font-size:12px; color:var(--text-soft); margin-bottom:8px;'>Non-linear model: showing global top feature stand-ins.</div>", unsafe_allow_html=True)
                            
                        if result['top_contributing_words']:
                            li_tags = "".join([f"<div class='annotations-list'>• {esc(w)}</div>" for w in result['top_contributing_words']])
                            st.markdown(f"<div>{li_tags}</div>", unsafe_allow_html=True)
                        else:
                            st.markdown("<div class='annotations-list'>No significant feature weights identified.</div>", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                                
                    with c2:
                        probs = result['probabilities']
                        df_probs = pd.DataFrame(list(probs.items()), columns=['Category', 'Probability']).sort_values('Probability')
                        fig = px.bar(df_probs, x='Probability', y='Category', orientation='h')
                        fig.update_layout(xaxis_range=[0,1], margin=dict(l=0, r=0, t=20, b=0), height=320,
                                          xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
                        fig.update_traces(marker_color='#B23A48')
                        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                        st.markdown(f"<div class='chart-caption'>Category probability distribution computed via {esc(selected_name)}.</div>", unsafe_allow_html=True)
                        
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    dispatch_note("error", "Dispatch failed to process through API.")

elif selected_page == "Correspondent Profiles":
    st.markdown("<h2>Correspondent Dossiers</h2>", unsafe_allow_html=True)
    selected_exp_name = st.selectbox("Select Correspondent", options=list(model_options.keys()), key="exp_select", label_visibility="collapsed")
    
    with st.spinner("Retrieving dossier..."):
        details = fetch_model_details(model_options[selected_exp_name])
        
    if details:
        c_left, c_right = st.columns([3, 2])
        
        with c_left:
            st.markdown(f"""
            <div style="display: flex; align-items: baseline; gap: 15px;">
                <h2 style="margin:0 !important; font-size:34px !important;">{esc(details['display_name'])}</h2>
                <span class="mono-tag">{esc(details['category'])}</span>
            </div>
            """, unsafe_allow_html=True)
            
            if 'how_it_differs' in details and details['how_it_differs']:
                st.markdown("<br>", unsafe_allow_html=True)
                dispatch_note("info", f"<b>DISTINCTION:</b> {esc(details['how_it_differs'])}")
                
            st.markdown(f"<p class='drop-cap'>{esc(details['explanation']['plain_language'])}</p>", unsafe_allow_html=True)
            
            st.markdown("<div class='notebook-box'>", unsafe_allow_html=True)
            st.latex(details['explanation']['formula'])
            st.markdown("</div>", unsafe_allow_html=True)
            
            p_col1, p_col2 = st.columns(2)
            with p_col1:
                st.markdown("<h3>Pros</h3>", unsafe_allow_html=True)
                for pro in details['pros']:
                    st.markdown(f"<div class='annotations-list'>[✓] {esc(pro)}</div>", unsafe_allow_html=True)
            with p_col2:
                st.markdown("<h3>Cons</h3>", unsafe_allow_html=True)
                for con in details['cons']:
                    st.markdown(f"<div class='annotations-list'>[x] {esc(con)}</div>", unsafe_allow_html=True)
                    
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"<div class='annotations-list' style='margin-bottom: 20px;'><b>OPTIMAL USE CASE:</b> {esc(details['best_for'])}</div>", unsafe_allow_html=True)

        with c_right:
            m = details['metrics']
            acc_pct = f"{m['accuracy']*100:.1f}%"
            
            st.markdown(f"""
            <div style="margin-bottom:20px;">
                <div class="hero-metric-num">{acc_pct}</div>
                <div class="hero-metric-label">Primary Accuracy Metric</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-inline-group">
                <div class="metric-inline-item">
                    <span class="metric-inline-val">{m['macro_f1']*100:.1f}%</span>
                    <span class="metric-inline-lbl">Macro F1</span>
                </div>
                <div style="border-left:1px dotted var(--rule); height:24px;"></div>
                <div class="metric-inline-item">
                    <span class="metric-inline-val">{m['macro_precision']*100:.1f}%</span>
                    <span class="metric-inline-lbl">Precision</span>
                </div>
                <div style="border-left:1px dotted var(--rule); height:24px;"></div>
                <div class="metric-inline-item">
                    <span class="metric-inline-val">{m['macro_recall']*100:.1f}%</span>
                    <span class="metric-inline-lbl">Recall</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<h3>Confusion Matrix</h3>", unsafe_allow_html=True)
            cm = np.array(m['confusion_matrix'])
            labels = m['labels_order']
            
            wine_scale = [
                [0.0, '#191B21'],
                [0.25, '#3B1F27'],
                [0.6, '#752533'],
                [1.0, '#B23A48']
            ]
            fig_cm = px.imshow(cm, x=labels, y=labels, color_continuous_scale=wine_scale, text_auto=True)
            fig_cm.update_layout(xaxis_title="PREDICTED", yaxis_title="ACTUAL", font=dict(family='IBM Plex Mono'),
                                margin=dict(l=0, r=0, t=20, b=0), height=300)
            st.plotly_chart(fig_cm, use_container_width=True, config={'displayModeBar': False})
            st.markdown(f"<div class='chart-caption'>Test set confusion matrix for {esc(details['display_name'])}.</div>", unsafe_allow_html=True)

elif selected_page == "Standings":
    st.markdown("<h2>Current Standings</h2>", unsafe_allow_html=True)
    leaderboard = fetch_leaderboard()
    
    if leaderboard:
        df_lb = pd.DataFrame(leaderboard)
        
        c1, c2 = st.columns([3, 2])
        with c1:
            fig_lb = go.Figure()
            fig_lb.add_trace(go.Bar(x=df_lb['display_name'], y=df_lb['accuracy'], name='Accuracy', marker_color='#2F6B55'))
            fig_lb.add_trace(go.Bar(x=df_lb['display_name'], y=df_lb['macro_f1'], name='Macro F1', marker_color='#C9A227'))
            fig_lb.update_layout(barmode='group', title="ACCURACY VS F1 SCORE", yaxis_range=[0,1],
                                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                                xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
            st.plotly_chart(fig_lb, use_container_width=True, config={'displayModeBar': False})
            st.markdown("<div class='chart-caption'>Standardized evaluation on 20% held-out test split (15,000 TF-IDF features).</div>", unsafe_allow_html=True)

        with c2:
            st.markdown("<h3>Leaderboard Summary</h3>", unsafe_allow_html=True)
            dispatch_note("info", "Linear SVM achieves highest accuracy overall on high-dimensional text vectors. Naive Bayes provides instant training with minimal accuracy drop. Decision Tree suffers from severe overfitting on sparse features.")
            
        st.markdown("<h2 style='margin-top:25px !important;'>Results Board</h2>", unsafe_allow_html=True)
        
        html_table = "<table style='width:100%; text-align:left; border-collapse: collapse;' class='stTable'><tr><th style='padding-bottom:10px;'>Rank</th><th style='padding-bottom:10px;'>Correspondent</th><th style='padding-bottom:10px;'>Accuracy</th><th style='padding-bottom:10px;'>Train Time</th><th style='padding-bottom:10px;'>Inference Time</th></tr>"
        for i, row in df_lb.iterrows():
            html_table += f"""
            <tr>
                <td class='lb-rank'>{(i+1):02d}</td>
                <td style='font-family: "IBM Plex Sans", sans-serif; font-weight: 600; font-size: 16px; color: var(--text);'>{esc(row['display_name'])}</td>
                <td>{row['accuracy']:.2%}</td>
                <td>{row['train_seconds']:.3f}s</td>
                <td>{row['avg_inference_ms']:.3f}ms</td>
            </tr>
            """
        html_table += "</table>"
        st.markdown(html_table, unsafe_allow_html=True)

elif selected_page == "All Hands on Deck":
    st.markdown("<h2>All Hands On Deck</h2>", unsafe_allow_html=True)
    compare_input = st.text_area("Dispatch Text", height=100, key="compare_input", label_visibility="collapsed", placeholder="Enter a story to see all 6 correspondents file a report...")
    
    if st.button("Request All Reports", use_container_width=True):
        if not compare_input.strip():
            dispatch_note("info", "Please enter a dispatch.")
        else:
            with st.spinner("Awaiting reports..."):
                results = predict_compare(compare_input)
                
                if results:
                    categories = [r['predicted_category'] for r in results]
                    majority_cat = max(set(categories), key=categories.count)
                    
                    st.markdown("<div class='reveal'>", unsafe_allow_html=True)
                    st.markdown(f"""
                    <div style="text-align:center; padding: 15px 0; border-bottom: 3px double var(--brass); margin-bottom: 25px;">
                        <div style="font-family:'IBM Plex Mono', monospace; font-size: 13px; color: var(--text-soft); margin-bottom:6px;">EDITORIAL CONSENSUS</div>
                        <h1 class="masthead-title" style="font-size: 56px;">{esc(majority_cat)}</h1>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    cols = st.columns(3)
                    for i, r in enumerate(results):
                        with cols[i % 3]:
                            agrees = r['predicted_category'] == majority_cat
                            icon = "<span class='agree-yes'>[✓] AGREES</span>" if agrees else "<span class='agree-no'>[x] DISAGREES</span>"
                            
                            st.markdown(f"""
                            <div class="telegram-slip">
                                <div class="slip-reporter">FILED BY: {esc(r['display_name'])}</div>
                                <div style="text-align:center;">
                                    {render_stamp(r['predicted_category'], r['confidence'])}
                                </div>
                                <div class="slip-agreement">{icon}</div>
                            </div>
                            <br>
                            """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    dispatch_note("error", "Failed to retrieve reports.")

elif selected_page == "Batch Wire":
    st.markdown("<h2>Batch Wire</h2>", unsafe_allow_html=True)
    st.markdown("Upload a CSV file containing a `headline` column to bulk-process dispatches through a correspondent.")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        selected_name = st.selectbox("Assign to Correspondent", options=list(model_options.keys()), index=list(model_options.keys()).index(default_model_name))
        run_all = st.checkbox("Run ALL Models (Consensus)")
    with col1:
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")
        
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            if 'headline' not in df.columns:
                dispatch_note("error", "CSV must contain a 'headline' column.")
            else:
                if st.button("Start Bulk Processing", use_container_width=True):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    results_data = []
                    total = len(df)
                    
                    max_process = min(total, 500)
                    if total > 500:
                        dispatch_note("info", f"Processing capped at first {max_process} rows.")
                        df = df.head(max_process)
                        total = max_process
                        
                    for i, row in df.iterrows():
                        text = str(row['headline'])
                        if 'short_description' in df.columns and pd.notna(row['short_description']):
                            text += " " + str(row['short_description'])
                            
                        if run_all:
                            res = predict_compare(text)
                            if res:
                                cats = [r['predicted_category'] for r in res]
                                majority_cat = max(set(cats), key=cats.count)
                                results_data.append(majority_cat)
                            else:
                                results_data.append("ERROR")
                        else:
                            res = predict(text, model_options[selected_name])
                            if res:
                                results_data.append(res['predicted_category'])
                            else:
                                results_data.append("ERROR")
                                
                        progress_bar.progress((i + 1) / total)
                        status_text.text(f"Processed {i+1}/{total} dispatches...")
                        
                    df['predicted_category'] = results_data
                    status_text.empty()
                    progress_bar.empty()
                    
                    dispatch_note("success", "Batch processing complete.")
                    
                    st.dataframe(df.head(50), use_container_width=True)
                    
                    csv_buffer = io.StringIO()
                    df.to_csv(csv_buffer, index=False)
                    st.download_button(
                        label="Download Results (CSV)",
                        data=csv_buffer.getvalue(),
                        file_name="batch_results.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
        except Exception as e:
            dispatch_note("error", f"Failed to process CSV file: {esc(e)}")

elif selected_page == "The Morgue":
    st.markdown("<h2>The Morgue</h2>", unsafe_allow_html=True)
    st.markdown("<p class='drop-cap'>Explore the historical archives. These entries represent ground-truth training records used to fit the models.</p>", unsafe_allow_html=True)
    
    if archive_df.empty:
        dispatch_note("error", "Archive dataset (news_data.csv) could not be loaded or found.")
    else:
        categories = sorted(archive_df['category'].unique().tolist())
        
        c1, c2 = st.columns([1, 2])
        with c1:
            cat_filter = st.selectbox("Filter by Category", ["All"] + categories)
        with c2:
            search_query = st.text_input("Search Archives", placeholder="Keyword search...")
            
        filtered_df = archive_df
        if cat_filter != "All":
            filtered_df = filtered_df[filtered_df['category'] == cat_filter]
        if search_query:
            filtered_df = filtered_df[filtered_df['headline'].str.contains(search_query, case=False, na=False) | filtered_df['short_description'].str.contains(search_query, case=False, na=False)]
            
        st.markdown(f"<div class='nav-group-title' style='margin-bottom:10px;'>SHOWING {len(filtered_df)} RECORDS</div>", unsafe_allow_html=True)
        
        for _, row in filtered_df.head(50).iterrows():
            cat_tag = esc(row['category'])
            h_text = esc(row['headline'])
            d_text = esc(row.get('short_description', ''))
            
            st.markdown(f"""
            <div class="archive-entry">
                <span class="mono-tag" style="float:right;">{cat_tag}</span>
                <div class="archive-title">{h_text}</div>
                <div class="archive-snippet">{d_text}</div>
            </div>
            """, unsafe_allow_html=True)
            
        if len(filtered_df) > 50:
            rem_count = len(filtered_df) - 50
            st.markdown(f"<div class='chart-caption'>... {rem_count} MORE RECORDS HIDDEN ...</div>", unsafe_allow_html=True)

elif selected_page == "Editor's Challenge":
    st.markdown("<h2>Editor's Challenge</h2>", unsafe_allow_html=True)
    
    if archive_df.empty:
        dispatch_note("error", "Archive dataset required for the challenge.")
    else:
        wins = st.session_state.challenge_wins
        played = st.session_state.challenge_played
        
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:flex-end;">
            <p>Can you beat the wire? Read the dispatch and guess its ground-truth category.</p>
            <span class="mono-tag" style="font-size:13px; border-color:var(--brass); color:var(--brass);">SCORE: {wins} / {played} CORRECT</span>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.current_challenge is None:
            idx = random.randint(0, len(archive_df) - 1)
            st.session_state.current_challenge = archive_df.iloc[idx].to_dict()
            st.session_state.challenge_revealed = False
            st.session_state.challenge_guess = None
            
        challenge = st.session_state.current_challenge
        c_headline = esc(challenge['headline'])
        c_desc = esc(challenge.get('short_description', ''))
        
        st.markdown(f"""
        <div class="pull-quote" style="font-size:22px; padding:20px; border-left: 6px solid var(--wine);">
            {c_headline}
            <div style="font-family:'IBM Plex Sans', sans-serif; font-size:15px; font-style:normal; color:var(--text-soft); margin-top:8px;">
                {c_desc}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.challenge_revealed:
            st.markdown("<h3>YOUR CALL, CHIEF:</h3>", unsafe_allow_html=True)
            categories = sorted(archive_df['category'].unique().tolist())
            cols = st.columns(5)
            for i, cat in enumerate(categories):
                if cols[i % 5].button(cat, key=f"guess_{cat}", use_container_width=True):
                    st.session_state.challenge_guess = cat
                    st.session_state.challenge_revealed = True
                    st.session_state.challenge_played += 1
                    if cat == challenge['category']:
                        st.session_state.challenge_wins += 1
                    st.rerun()
                    
        else:
            guess = st.session_state.challenge_guess
            true_cat = challenge['category']
            
            is_correct = (guess == true_cat)
            msg = f"SPOT ON. YOU BEAT THE WIRE." if is_correct else f"INCORRECT. THE TRUE CATEGORY IS <b>{esc(true_cat)}</b>."
            dispatch_note("success" if is_correct else "error", msg)
            
            st.markdown("<h3>THE WIRE'S VERDICTS:</h3>", unsafe_allow_html=True)
            text_to_predict = str(challenge['headline']) + " " + str(challenge.get('short_description', ''))
            
            with st.spinner("Gathering correspondent verdicts..."):
                results = predict_compare(text_to_predict)
                
            if results:
                cols = st.columns(6)
                for i, r in enumerate(results):
                    with cols[i]:
                        st.markdown(f"<div style='text-align:center; font-family:\"IBM Plex Mono\", monospace; font-size:11px; margin-bottom:5px; color:var(--text-soft);'>{esc(r['display_name'])}</div>", unsafe_allow_html=True)
                        st.markdown(render_stamp(r['predicted_category']), unsafe_allow_html=True)
                        if r['predicted_category'] == true_cat:
                            st.markdown("<div style='text-align:center; color:var(--emerald); font-size:14px; font-weight:bold;'>✓</div>", unsafe_allow_html=True)
                        else:
                            st.markdown("<div style='text-align:center; color:var(--wine); font-size:14px; font-weight:bold;'>✗</div>", unsafe_allow_html=True)
                            
            if st.button("PULL NEXT DISPATCH", use_container_width=True):
                st.session_state.current_challenge = None
                st.rerun()

elif selected_page == "Head-to-Head":
    st.markdown("<h2>Head-to-Head</h2>", unsafe_allow_html=True)
    st.markdown("Pitch two correspondents against each other to compare probability distributions in detail.")
    
    leaderboard_data = fetch_leaderboard()
    model2_default_idx = 1
    if leaderboard_data:
        other_models = [m for m in leaderboard_data if m['display_name'] != default_model_name]
        if other_models:
            top_other = max(other_models, key=lambda x: x.get('accuracy', 0))
            top_other_name = top_other['display_name']
            if top_other_name in list(model_options.keys()):
                model2_default_idx = list(model_options.keys()).index(top_other_name)
                
    col1, col2 = st.columns(2)
    with col1:
        model1 = st.selectbox("Correspondent 1", options=list(model_options.keys()), index=0)
    with col2:
        model2 = st.selectbox("Correspondent 2", options=list(model_options.keys()), index=model2_default_idx)
        
    text_input = st.text_area("Dispatch Text", height=100, label_visibility="collapsed", placeholder="Enter text to analyze...")
    
    if st.button("Compare Correspondents", use_container_width=True):
        if not text_input.strip():
            dispatch_note("info", "Please enter a story dispatch.")
        elif model1 == model2:
            dispatch_note("error", "Please select two different correspondents.")
        else:
            with st.spinner("Analyzing..."):
                res1 = predict(text_input, model_options[model1])
                res2 = predict(text_input, model_options[model2])
                
                if res1 and res2:
                    st.markdown("<div class='reveal'>", unsafe_allow_html=True)
                    
                    cat1 = res1['predicted_category']
                    cat2 = res2['predicted_category']
                    
                    if cat1 == cat2:
                        diff = abs(res1['confidence'] - res2['confidence']) * 100
                        msg = f"<b>CONSENSUS REACHED.</b> Both agree on <b>{esc(cat1)}</b>, with confidence variance of {diff:.1f}%."
                        dispatch_note("success", msg)
                    else:
                        msg = f"<b>DISAGREEMENT.</b> {esc(model1)} favors <b>{esc(cat1)}</b> ({res1['confidence']*100:.1f}%) while {esc(model2)} favors <b>{esc(cat2)}</b> ({res2['confidence']*100:.1f}%)."
                        dispatch_note("error", msg)
                        
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f"<div style='text-align:center;'><div class='nav-group-title'>{esc(model1)}</div>", unsafe_allow_html=True)
                        st.markdown(render_stamp(cat1, res1['confidence']), unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                    with c2:
                        st.markdown(f"<div style='text-align:center;'><div class='nav-group-title'>{esc(model2)}</div>", unsafe_allow_html=True)
                        st.markdown(render_stamp(cat2, res2['confidence']), unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                    st.markdown("<h3>Probability Distributions</h3>", unsafe_allow_html=True)
                    
                    p1 = pd.DataFrame(list(res1['probabilities'].items()), columns=['Category', 'Probability'])
                    p1['Model'] = model1
                    p2 = pd.DataFrame(list(res2['probabilities'].items()), columns=['Category', 'Probability'])
                    p2['Model'] = model2
                    df_merged = pd.concat([p1, p2])
                    
                    fig = px.bar(df_merged, x='Category', y='Probability', color='Model', barmode='group',
                                 color_discrete_sequence=['#B23A48', '#2F6B55'])
                    fig.update_layout(yaxis_range=[0,1], legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                                      xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                    st.markdown(f"<div class='chart-caption'>Side-by-side category probability comparison for {esc(model1)} vs {esc(model2)}.</div>", unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    dispatch_note("error", "Failed to retrieve reports from API.")
