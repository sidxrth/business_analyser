import streamlit as st
import subprocess
import sys

st.set_page_config(
    page_title="Business Analytics Platform",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Query param handling (modern Streamlit API) ---
if "mode" in st.query_params:
    mode = st.query_params["mode"]
    if mode == "simple":
        subprocess.Popen([sys.executable, "-m", "streamlit", "run", "simple_app.py"])
        st.stop()
    elif mode == "analyst":
        subprocess.Popen([sys.executable, "-m", "streamlit", "run", "app.py"])
        st.stop()

# --- Color Palette ---
PRIMARY_BLUE = "#2C5F8D"
PRIMARY_LIGHT = "#E8F1F8"
ACCENT_TEAL = "#1B7F79"
ACCENT_CORAL = "#D96846"
SURFACE_WHITE = "#FFFFFF"
SURFACE_GRAY = "#F5F7FA"
TEXT_DARK = "#1A1A1A"
TEXT_MEDIUM = "#4A5568"
BORDER_LIGHT = "#D1D9E6"

# --- CSS Styling ---
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&display=swap');
* {{ font-family: 'Rajdhani', sans-serif !important; }}
.main {{
    background: linear-gradient(135deg, {SURFACE_WHITE} 0%, {PRIMARY_LIGHT} 100%);
    color: {TEXT_DARK};
}}
.stApp {{
    background: linear-gradient(135deg, {SURFACE_WHITE} 0%, {PRIMARY_LIGHT} 100%);
}}
.mode-card {{
    background: {SURFACE_WHITE};
    border-radius: 16px;
    padding: 40px 32px;
    margin: 20px 0;
    border: 2px solid {BORDER_LIGHT};
    transition: all 0.4s ease;
    position: relative;
    overflow: hidden;
    cursor: pointer;
}}
.mode-card:hover {{
    transform: translateY(-8px);
    box-shadow: 0 8px 24px rgba(44,95,141,0.2);
}}
.mode-title {{
    font-size: 2rem;
    font-weight: 700;
    color: {PRIMARY_BLUE};
    margin-bottom: 16px;
}}
.mode-description {{
    font-size: 1.05rem;
    color: {TEXT_DARK}; /* Changed to blackish text */
    margin-bottom: 12px;
    line-height: 1.6;
}}
.mode-points {{
    text-align: left;
    color: {TEXT_DARK};
    font-size: 1rem;
    margin-top: 10px;
    margin-bottom: 16px;
    padding-left: 20px;
}}
.mode-points li {{
    margin: 6px 0;
    list-style-type: "▸ ";
    font-weight: 500;
}}
.stButton > button {{
    background: linear-gradient(135deg, {ACCENT_TEAL}, {PRIMARY_BLUE});
    color: white;
    border: none;
    padding: 16px 48px;
    border-radius: 8px;
    font-weight: 700;
    transition: all 0.3s ease;
}}
.stButton > button:hover {{
    transform: scale(1.05);
}}
</style>
""", unsafe_allow_html=True)

# --- Layout ---
col1, col2 = st.columns(2, gap="large")

# SIMPLE MODE CARD
with col1:
    st.markdown(f"""
    <div class='mode-card'>
        <div class='mode-title'>BEGINNER MODE</div>
        <div class='mode-description'>
            Streamlined interface for quick insights and easy analytics.
        </div>
        <ul class='mode-points'>
            <li>Intuitive one-click navigation</li>
            <li>Essential KPIs at a glance</li>
            <li>Clean visuals for better clarity</li>
            <li>No setup required — plug & play</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    if st.button("LAUNCH BEGINNER MODE", use_container_width=True):
        st.query_params["mode"] = "simple"
        subprocess.Popen([sys.executable, "-m", "streamlit", "run", "simple_app.py"])
        st.stop()

# ANALYST MODE CARD
with col2:
    st.markdown(f"""
    <div class='mode-card'>
        <div class='mode-title'>BUSSINESS MODE</div>
        <div class='mode-description'>
            Comprehensive analytical environment for professional insights and advanced data exploration.
        </div>
        <ul class='mode-points'>
            <li>RFM segmentation & KPI tracking</li>
            <li>Advanced visualizations with Plotly</li>
            <li>Regional and product-based analytics</li>
            <li>Data-driven strategy dashboards</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    if st.button("LAUNCH BUSINESS MODE", use_container_width=True):
        st.query_params["mode"] = "analyst"
        subprocess.Popen([sys.executable, "-m", "streamlit", "run", "app.py"])
        st.stop()
