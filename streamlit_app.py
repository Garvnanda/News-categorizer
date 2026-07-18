import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np

# Page config must be the first Streamlit command
st.set_page_config(page_title="The Wire Room", page_icon="📰", layout="wide")

API_URL = "http://127.0.0.1:8001"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Anton&family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;600;700&display=swap');

:root {
    --paper: #F6F3EC;
    --paper-raised: #FFFFFF;
    --ink: #20242B;
    --ink-soft: #5B5F68;
    --rule: #D8D2C4;
    --stamp-red: #A6283C;
    --wire-teal: #2E6659;
    --gold: #C79A3A;
}

/* Hide Streamlit Chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Base typography overrides */
html, body, [class*="css"]  {
    font-family: 'IBM Plex Sans', sans-serif;
    color: var(--ink);
}

/* Masthead */
.masthead-title {
    font-family: 'Anton', sans-serif;
    font-size: 48px;
    letter-spacing: 0.02em;
    color: var(--ink);
    margin-bottom: 0;
    line-height: 1;
}
.masthead-subtitle {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 14px;
    text-transform: uppercase;
    color: var(--ink-soft);
    letter-spacing: 0.05em;
    margin-top: 5px;
    margin-bottom: 10px;
}
.masthead-rule {
    border-top: 1px solid var(--ink);
    border-bottom: 1px solid var(--ink);
    height: 4px;
    margin-bottom: 30px;
}
.wire-status {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 14px;
    font-weight: 600;
}

/* Headers */
h1, h2, h3 {
    font-family: 'IBM Plex Sans', sans-serif;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--ink);
}
h1 { font-size: 28px !important; }
h2 { font-size: 22px !important; margin-top: 1.5rem !important; margin-bottom: 1rem !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 2rem;
    border-bottom: 1px solid var(--rule);
}
.stTabs [data-baseweb="tab"] {
    font-family: 'IBM Plex Sans', sans-serif !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-size: 14px !important;
    color: var(--ink-soft) !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    background: transparent !important;
    padding-bottom: 10px !important;
    padding-top: 10px !important;
}
.stTabs [aria-selected="true"] {
    color: var(--ink) !important;
    border-bottom: 2px solid var(--stamp-red) !important;
    font-weight: 700 !important;
}

/* Buttons */
.stButton>button {
    border-radius: 2px !important;
    border: 1px solid var(--ink) !important;
    color: var(--ink) !important;
    background-color: transparent !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    font-weight: 600 !important;
    transition: all 0.2s ease-in-out !important;
}
.stButton>button:hover {
    background-color: var(--stamp-red) !important;
    border-color: var(--stamp-red) !important;
    color: white !important;
}

/* Inputs */
.stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
    border-radius: 2px !important;
    border: 1px solid var(--rule) !important;
    background-color: var(--paper-raised) !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    color: var(--ink) !important;
}
.stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus, .stSelectbox>div>div>div:focus-within {
    border-color: var(--stamp-red) !important;
    box-shadow: 0 0 0 1px var(--stamp-red) !important;
}

/* Custom Components */
.stat-card {
    background-color: var(--paper-raised);
    border: 1px solid var(--rule);
    padding: 15px;
    border-radius: 2px;
}
.stat-card-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    text-transform: uppercase;
    color: var(--ink-soft);
    margin-bottom: 5px;
}
.stat-card-value {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 32px;
    font-weight: 700;
    color: var(--ink);
    line-height: 1.1;
}

.dispatch-note {
    background-color: var(--paper-raised);
    padding: 12px 15px;
    border-radius: 2px;
    margin-bottom: 1rem;
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 15px;
}
.dispatch-note-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 4px;
    display: block;
}
.dispatch-success { border-left: 4px solid var(--wire-teal); }
.dispatch-error { border-left: 4px solid var(--stamp-red); }
.dispatch-info { border-left: 4px solid var(--gold); }
.dispatch-success .dispatch-note-label { color: var(--wire-teal); }
.dispatch-error .dispatch-note-label { color: var(--stamp-red); }
.dispatch-info .dispatch-note-label { color: var(--gold); }

.stamp-badge {
    display: inline-block;
    border: 3px solid var(--stamp-red);
    color: var(--stamp-red);
    font-family: 'Anton', sans-serif;
    text-transform: uppercase;
    font-size: 24px;
    padding: 2px 12px;
    border-radius: 3px 8px 4px 9px;
    transform: rotate(-3deg);
    line-height: 1.2;
    letter-spacing: 0.05em;
    opacity: 0.9;
}
.stamp-container {
    text-align: center;
    display: inline-block;
    margin: 10px 0;
}
.stamp-conf {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: var(--ink-soft);
    margin-top: 5px;
    display: block;
}

/* Telegram Slip */
.telegram-slip {
    background-color: var(--paper-raised);
    border: 1px solid var(--rule);
    padding: 15px;
    border-radius: 2px;
    height: 100%;
    transition: transform 0.2s ease-out, box-shadow 0.2s ease-out;
}
.telegram-slip:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
.slip-reporter {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: var(--ink-soft);
    text-transform: uppercase;
    margin-bottom: 15px;
    border-bottom: 1px dotted var(--rule);
    padding-bottom: 5px;
}
.slip-agreement {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 16px;
    font-weight: 600;
    margin-top: 15px;
    text-align: center;
}
.agree-yes { color: var(--wire-teal); }
.agree-no { color: var(--stamp-red); }

/* Notebook Box */
.notebook-box {
    background-color: var(--paper-raised);
    border: 1px dashed var(--rule);
    padding: 20px;
    border-radius: 2px;
    margin: 15px 0;
}

/* Pull Quote */
.pull-quote {
    font-family: 'IBM Plex Sans', serif;
    font-size: 18px;
    border-left: 4px solid var(--rule);
    padding-left: 15px;
    margin: 20px 0;
    color: var(--ink);
    line-height: 1.5;
}

/* Dataframe/Table overrides */
.stTable {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 14px;
}
.stTable th {
    font-family: 'IBM Plex Sans', sans-serif !important;
    color: var(--ink-soft) !important;
    border-bottom: 1px solid var(--ink) !important;
    text-transform: uppercase;
    font-size: 12px;
}
.stTable td {
    border-bottom: 1px solid var(--rule) !important;
}

/* Leaderboard Rank */
.lb-rank {
    font-family: 'Anton', sans-serif;
    font-size: 32px;
    color: var(--ink-soft);
    opacity: 0.5;
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

/* Annotations list */
.annotations-list {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    list-style-type: none;
    color: var(--ink);
    margin-bottom: 4px;
}

.mono-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    border: 1px solid var(--ink-soft);
    color: var(--ink-soft);
    padding: 2px 6px;
    border-radius: 2px;
    text-transform: uppercase;
}

</style>
""", unsafe_allow_html=True)

# Custom Plotly Template
colors = ['#2E6659', '#C79A3A', '#A6283C', '#20242B', '#5B5F68', '#D8D2C4', '#8A4F3D', '#4A7A7B']
pio.templates["wireroom"] = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor='#F6F3EC',
        plot_bgcolor='#F6F3EC',
        font=dict(family='IBM Plex Sans, sans-serif', color='#20242B'),
        colorway=colors,
        xaxis=dict(gridcolor='#D8D2C4', zerolinecolor='#D8D2C4'),
        yaxis=dict(gridcolor='#D8D2C4', zerolinecolor='#D8D2C4'),
    )
)
pio.templates.default = "wireroom"

# Custom component helpers
def stat_card(label, value):
    return f"""
    <div class="stat-card">
        <div class="stat-card-label">{label}</div>
        <div class="stat-card-value">{value}</div>
    </div>
    """

def dispatch_note(msg_type, msg):
    type_class = f"dispatch-{msg_type.lower()}"
    label = "DISPATCH" if msg_type.lower() == 'success' else msg_type.upper()
    st.markdown(f"""
    <div class="dispatch-note {type_class}">
        <span class="dispatch-note-label">{label}</span>
        {msg}
    </div>
    """, unsafe_allow_html=True)

def render_stamp(category: str, confidence: float | None = None) -> str:
    conf_html = f'<span class="stamp-conf">{confidence*100:.1f}% CONFIDENCE</span>' if confidence is not None else ''
    return f"""
    <div class="stamp-container">
        <div class="stamp-badge">{category}</div>
        {conf_html}
    </div>
    """

# API Calls
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

# Masthead
models = fetch_models()
wire_status = "<span class='wire-status' style='color: var(--wire-teal);'>● WIRE ACTIVE</span>" if models else "<span class='wire-status' style='color: var(--stamp-red);'>● DESK OFFLINE</span>"

st.markdown(f"""
<div style="display: flex; justify-content: space-between; align-items: flex-end;">
    <div>
        <h1 class="masthead-title">THE WIRE ROOM</h1>
        <div class="masthead-subtitle">AN EDITORIAL DESK FOR MACHINE LEARNING · 6 CORRESPONDENTS ON DUTY</div>
    </div>
    <div style="padding-bottom: 10px;">{wire_status}</div>
</div>
<div class="masthead-rule"></div>
""", unsafe_allow_html=True)

if not models:
    dispatch_note("error", "Cannot connect to the backend. Please ensure uvicorn is running on port 8001.")
    st.stop()

tab1, tab2, tab3, tab4 = st.tabs(["FILE A STORY", "CORRESPONDENT PROFILES", "STANDINGS", "ALL HANDS ON DECK"])

model_options = {m['display_name']: m['model_id'] for m in models}
default_model_name = next((m['display_name'] for m in models if m['model_id'] == 'logistic_regression'), list(model_options.keys())[0])

# --- PAGE 1: Predict ---
with tab1:
    st.markdown("<h2>File a story to the desk</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        text_input = st.text_area("News Text", height=150, label_visibility="collapsed", placeholder="Enter a headline or dispatch to be classified...")
    with col2:
        selected_name = st.selectbox("Assign to Correspondent", options=list(model_options.keys()), index=list(model_options.keys()).index(default_model_name), label_visibility="collapsed")
        predict_btn = st.button("File Dispatch", use_container_width=True)
        
    if predict_btn:
        if not text_input.strip():
            dispatch_note("info", "Please enter a dispatch before filing.")
        else:
            with st.spinner("Processing..."):
                result = predict(text_input, model_options[selected_name])
                if result:
                    st.markdown("<div class='reveal'>", unsafe_allow_html=True)
                    dispatch_note("success", "Dispatch received and categorized.")
                    
                    c1, c2 = st.columns([1, 2])
                    with c1:
                        st.markdown("<div class='stat-card' style='text-align: center;'>", unsafe_allow_html=True)
                        st.markdown(render_stamp(result['predicted_category'], result['confidence']), unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        is_linear = model_options[selected_name] in ['logistic_regression', 'naive_bayes', 'linear_svm']
                        expander_title = "Exact Contribution Words" if is_linear else "Typical Category Words"
                        
                        st.markdown(f"<div class='stat-card'><div class='stat-card-label'>{expander_title}</div>", unsafe_allow_html=True)
                        if not is_linear:
                            st.markdown("<div style='font-size:12px; color:var(--ink-soft); margin-bottom:8px;'>Non-linear model: showing global stand-in features.</div>", unsafe_allow_html=True)
                            
                        if result['top_contributing_words']:
                            li_tags = "".join([f"<div class='annotations-list'>+ {w}</div>" for w in result['top_contributing_words']])
                            st.markdown(f"<div>{li_tags}</div>", unsafe_allow_html=True)
                        else:
                            st.markdown("<div class='annotations-list'>No strong features found.</div>", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                                
                    with c2:
                        probs = result['probabilities']
                        df_probs = pd.DataFrame(list(probs.items()), columns=['Category', 'Probability']).sort_values('Probability')
                        fig = px.bar(df_probs, x='Probability', y='Category', orientation='h', title="PROBABILITY DISTRIBUTION")
                        fig.update_layout(xaxis_range=[0,1], margin=dict(l=0, r=0, t=30, b=0), height=350)
                        fig.update_traces(marker_color='#2E6659')
                        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    dispatch_note("error", "Dispatch failed to process.")

# --- PAGE 2: Model Explorer ---
with tab2:
    st.markdown("<h2>Correspondent Dossiers</h2>", unsafe_allow_html=True)
    selected_exp_name = st.selectbox("Select Correspondent", options=list(model_options.keys()), key="exp_select", label_visibility="collapsed")
    
    with st.spinner("Retrieving dossier..."):
        details = fetch_model_details(model_options[selected_exp_name])
        
    if details:
        st.markdown(f"""
        <div style="display: flex; align-items: baseline; gap: 15px; margin-top: 20px;">
            <h2 style="margin:0 !important; font-size:32px !important;">{details['display_name']}</h2>
            <span class="mono-tag">{details['category']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        if 'how_it_differs' in details and details['how_it_differs']:
            st.markdown("<br>", unsafe_allow_html=True)
            dispatch_note("info", f"<b>DISTINCTION:</b> {details['how_it_differs']}")
            
        st.markdown(f"<div class='pull-quote'>{details['explanation']['plain_language']}</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='notebook-box'>", unsafe_allow_html=True)
        st.latex(details['explanation']['formula'])
        st.markdown("</div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<h3>Pros</h3>", unsafe_allow_html=True)
            for pro in details['pros']:
                st.markdown(f"<div class='annotations-list'>[✓] {pro}</div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<h3>Cons</h3>", unsafe_allow_html=True)
            for con in details['cons']:
                st.markdown(f"<div class='annotations-list'>[x] {con}</div>", unsafe_allow_html=True)
                
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"<div class='annotations-list' style='margin-bottom: 20px;'><b>OPTIMAL ASSIGNMENT:</b> {details['best_for']}</div>", unsafe_allow_html=True)
        
        st.markdown("<h2>Performance Metrics</h2>", unsafe_allow_html=True)
        m = details['metrics']
        mc1, mc2, mc3, mc4 = st.columns(4)
        mc1.markdown(stat_card("Accuracy", f"{m['accuracy']*100:.1f}%"), unsafe_allow_html=True)
        mc2.markdown(stat_card("Macro F1", f"{m['macro_f1']*100:.1f}%"), unsafe_allow_html=True)
        mc3.markdown(stat_card("Macro Precision", f"{m['macro_precision']*100:.1f}%"), unsafe_allow_html=True)
        mc4.markdown(stat_card("Macro Recall", f"{m['macro_recall']*100:.1f}%"), unsafe_allow_html=True)
        
        st.markdown("<h2>Confusion Matrix</h2>", unsafe_allow_html=True)
        cm = np.array(m['confusion_matrix'])
        labels = m['labels_order']
        # Custom red scale: paper to stamp-red
        red_scale = [[0.0, '#F6F3EC'], [1.0, '#A6283C']]
        fig_cm = px.imshow(cm, x=labels, y=labels, color_continuous_scale=red_scale, text_auto=True)
        fig_cm.update_layout(xaxis_title="PREDICTED", yaxis_title="ACTUAL", font=dict(family='IBM Plex Mono'))
        st.plotly_chart(fig_cm, use_container_width=True)


# --- PAGE 3: Leaderboard ---
with tab3:
    st.markdown("<h2>Current Standings</h2>", unsafe_allow_html=True)
    leaderboard = fetch_leaderboard()
    
    if leaderboard:
        df_lb = pd.DataFrame(leaderboard)
        
        fig_lb = go.Figure()
        fig_lb.add_trace(go.Bar(x=df_lb['display_name'], y=df_lb['accuracy'], name='Accuracy', marker_color='#2E6659'))
        fig_lb.add_trace(go.Bar(x=df_lb['display_name'], y=df_lb['macro_f1'], name='Macro F1', marker_color='#C79A3A'))
        fig_lb.update_layout(barmode='group', title="ACCURACY VS F1 SCORE", yaxis_range=[0,1], legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_lb, use_container_width=True)
        
        st.markdown("<h2>Results Board</h2>", unsafe_allow_html=True)
        
        # Render a custom HTML table for the leaderboard to incorporate the big rank numbers
        html_table = "<table style='width:100%; text-align:left; border-collapse: collapse;' class='stTable'><tr><th style='padding-bottom:10px;'>Rank</th><th style='padding-bottom:10px;'>Correspondent</th><th style='padding-bottom:10px;'>Accuracy</th><th style='padding-bottom:10px;'>Train Time</th><th style='padding-bottom:10px;'>Inference Time</th></tr>"
        for i, row in df_lb.iterrows():
            html_table += f"""
            <tr>
                <td class='lb-rank'>{(i+1):02d}</td>
                <td style='font-family: "IBM Plex Sans", sans-serif; font-weight: 600; font-size: 16px;'>{row['display_name']}</td>
                <td>{row['accuracy']:.2%}</td>
                <td>{row['train_seconds']:.3f}s</td>
                <td>{row['avg_inference_ms']:.3f}ms</td>
            </tr>
            """
        html_table += "</table>"
        st.markdown(html_table, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        dispatch_note("info", "Linear SVM has the highest accuracy on our sparse TF-IDF vectors. Naive Bayes trains significantly faster with only a small accuracy trade-off. KNN is both the slowest at inference and least accurate here — a natural fit for discussing the 'curse of dimensionality'.")

# --- PAGE 4: Compare Models ---
with tab4:
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
                    <div style="text-align:center; padding: 20px 0; border-bottom: 4px solid var(--ink); margin-bottom: 30px;">
                        <div style="font-family:'IBM Plex Mono', monospace; font-size: 14px; color: var(--ink-soft); margin-bottom:10px;">CONSENSUS REACHED</div>
                        <h1 class="masthead-title" style="font-size: 64px;">{majority_cat}</h1>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    cols = st.columns(3)
                    for i, r in enumerate(results):
                        with cols[i % 3]:
                            agrees = r['predicted_category'] == majority_cat
                            icon = "<span class='agree-yes'>[✓] AGREES</span>" if agrees else "<span class='agree-no'>[x] DISAGREES</span>"
                            
                            st.markdown(f"""
                            <div class="telegram-slip">
                                <div class="slip-reporter">FILED BY: {r['display_name']}</div>
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
