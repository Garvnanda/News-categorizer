import streamlit as st
import requests

st.set_page_config(page_title="News Classifier", page_icon="📰")

# Sidebar for settings
st.sidebar.header("⚙️ Settings")
backend_url = st.sidebar.text_input(
    "Backend API URL", 
    value="http://127.0.0.1:8000",
    help="Enter the URL where the FastAPI backend is running."
)

st.sidebar.markdown("### Backend Connection Status")
try:
    # Try hitting the OpenAPI docs endpoint which FastAPI auto-generates
    health_check = requests.get(f"{backend_url.rstrip('/')}/docs", timeout=2)
    if health_check.status_code == 200:
        st.sidebar.success("✅ Connected to backend!")
    else:
        st.sidebar.warning("⚠️ Connected, but received unexpected status.")
except requests.exceptions.ConnectionError:
    st.sidebar.error("❌ Could not connect. Is the API running?")
except Exception as e:
    st.sidebar.error(f"❌ Connection error: {e}")

# Main UI
st.title("📰 News Category Classifier")
st.markdown("Enter a news headline or short description below, and the machine learning model will predict its category.")

text_input = st.text_area("News Text", height=150, placeholder="Type your news headline here...")

if st.button("Predict Category"):
    if text_input.strip():
        with st.spinner("Analyzing text..."):
            try:
                # Use the customizable backend URL
                predict_endpoint = f"{backend_url.rstrip('/')}/predict"
                response = requests.post(predict_endpoint, json={"text": text_input}, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"**Predicted Category:** {result['category']}")
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")
            except requests.exceptions.ConnectionError:
                st.error(f"Could not connect to the API at {predict_endpoint}. Please ensure the server is running.")
    else:
        st.warning("Please enter some text to classify.")
