import streamlit as st
import os

st.set_page_config(
    page_title="Business Analytics Platform",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Light Premium Color Palette
PRIMARY_BLUE = "#2C5F8D"
PRIMARY_LIGHT = "#E8F1F8"
ACCENT_TEAL = "#1B7F79"
ACCENT_CORAL = "#D96846"
SURFACE_WHITE = "#FFFFFF"
SURFACE_GRAY = "#F5F7FA"
TEXT_DARK = "#1A1A1A"
TEXT_MEDIUM = "#4A5568"
BORDER_LIGHT = "#D1D9E6"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&display=swap');

* {{
    font-family: 'Rajdhani', sans-serif !important;
}}

.main {{
    background: linear-gradient(135deg, {SURFACE_WHITE} 0%, {PRIMARY_LIGHT} 100%);
    color: {TEXT_DARK};
}}

.stApp {{
    background: linear-gradient(135deg, {SURFACE_WHITE} 0%, {PRIMARY_LIGHT} 100%);
}}

/* Hero Section - Removed from output, but keeping styles here in case they are used elsewhere */
.hero-container {{
    text-align: center;
    padding: 60px 20px 40px 20px;
    background: linear-gradient(135deg, {PRIMARY_BLUE} 0%, {ACCENT_TEAL} 100%);
    border-radius: 16px;
    margin-bottom: 50px;
    box-shadow: 0 8px 32px rgba(44, 95, 141, 0.2);
}}

.hero-title {{
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 3.5rem;
    font-weight: 700;
    color: {SURFACE_WHITE};
    margin-bottom: 16px;
    letter-spacing: 1px;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}}

.hero-subtitle {{
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.3rem;
    font-weight: 400;
    color: rgba(255, 255, 255, 0.9);
    letter-spacing: 0.5px;
}}

/* Mode Selection Cards */
.mode-card {{
    background: {SURFACE_WHITE};
    border-radius: 16px;
    padding: 40px 32px;
    margin: 20px 0;
    border: 2px solid {BORDER_LIGHT};
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    cursor: pointer;
    height: 100%;
    min-height: 320px;
}}

.mode-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 6px;
    background: linear-gradient(90deg, {ACCENT_TEAL}, {PRIMARY_BLUE});
    transform: scaleX(0);
    transition: transform 0.4s ease;
}}

.mode-card:hover::before {{
    transform: scaleX(1);
}}

.mode-card:hover {{
    transform: translateY(-12px);
    box-shadow: 0 16px 48px rgba(44, 95, 141, 0.2);
    border: 2px solid {PRIMARY_BLUE};
}}

.mode-icon {{
    font-size: 4rem;
    margin-bottom: 20px;
    display: block;
}}

.mode-title {{
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 2rem;
    font-weight: 700;
    color: {PRIMARY_BLUE};
    margin-bottom: 16px;
    letter-spacing: 0.5px;
}}

.mode-description {{
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.1rem;
    font-weight: 400;
    color: {TEXT_MEDIUM};
    line-height: 1.7;
    margin-bottom: 24px;
}}

.mode-features {{
    text-align: left;
    margin-top: 24px;
    padding-top: 24px;
    border-top: 1px solid {BORDER_LIGHT};
}}

.feature-item {{
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem;
    color: {TEXT_DARK};
    margin: 12px 0;
    padding-left: 24px;
    position: relative;
}}

.feature-item::before {{
    content: '▸';
    position: absolute;
    left: 0;
    color: {ACCENT_TEAL};
    font-weight: 700;
}}

/* Enhanced Buttons */
.stButton > button {{
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.2rem;
    font-weight: 700;
    padding: 16px 48px;
    border-radius: 8px;
    border: none;
    letter-spacing: 1px;
    text-transform: uppercase;
    transition: all 0.3s ease;
    width: 100%;
    box-shadow: 0 4px 16px rgba(44, 95, 141, 0.2);
}}

.simple-button {{
    background: linear-gradient(135deg, {ACCENT_TEAL} 0%, {PRIMARY_BLUE} 100%);
    color: {SURFACE_WHITE};
}}

.analyst-button {{
    background: linear-gradient(135deg, {PRIMARY_BLUE} 0%, {ACCENT_CORAL} 100%);
    color: {SURFACE_WHITE};
}}

.stButton > button:hover {{
    transform: scale(1.05);
    box-shadow: 0 8px 24px rgba(44, 95, 141, 0.3);
}}

/* Info Footer - Removed from output, but keeping styles here in case they are used elsewhere */
.info-footer {{
    background: {SURFACE_WHITE};
    border-radius: 12px;
    padding: 32px;
    margin-top: 50px;
    border: 1px solid {BORDER_LIGHT};
    box-shadow: 0 2px 12px rgba(44, 95, 141, 0.08);
}}

.info-section {{
    display: flex;
    align-items: start;
    margin: 20px 0;
    padding: 16px;
    background: {SURFACE_GRAY};
    border-radius: 8px;
    border-left: 4px solid {ACCENT_TEAL};
}}

.info-icon {{
    font-size: 1.8rem;
    margin-right: 16px;
    min-width: 40px;
}}

.info-content {{
    flex: 1;
}}

.info-title {{
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.2rem;
    font-weight: 700;
    color: {PRIMARY_BLUE};
    margin-bottom: 8px;
}}

.info-text {{
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.05rem;
    font-weight: 400;
    color: {TEXT_MEDIUM};
    line-height: 1.6;
}}

/* Divider */
hr {{
    border: none;
    height: 2px;
    background: linear-gradient(90deg, transparent, {BORDER_LIGHT}, transparent);
    margin: 40px 0;
}}

h1, h2, h3, p {{
    font-family: 'Rajdhani', sans-serif !important;
}}
</style>
""", unsafe_allow_html=True)

# Hero Section (Removed)

# Mode Selection Cards
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class='mode-card'>
        <span class='mode-icon'>◐</span>
        <div class='mode-title'>SIMPLE MODE</div>
        <div class='mode-description'>
            Streamlined interface designed for quick insights and accessible data exploration without technical complexity.
        </div>
        <div class='mode-features'>
            <div class='feature-item'>Visual storytelling approach</div>
            <div class='feature-item'>Intuitive card-based layouts</div>
            <div class='feature-item'>Simplified metrics display</div>
            <div class='feature-item'>User-friendly navigation</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Updated class for button style consistency after hero removal
    if st.button("LAUNCH SIMPLE MODE", key="simple", use_container_width=True):
        os.system("streamlit run simple_app.py")

with col2:
    st.markdown("""
    <div class='mode-card'>
        <span class='mode-icon'>◈</span>
        <div class='mode-title'>ANALYST MODE</div>
        <div class='mode-description'>
            Comprehensive analytical environment with advanced visualizations and deep-dive capabilities for data professionals.
        </div>
        <div class='mode-features'>
            <div class='feature-item'>Advanced chart libraries</div>
            <div class='feature-item'>Detailed KPI breakdowns</div>
            <div class='feature-item'>Segmentation analytics</div>
            <div class='feature-item'>Technical metrics suite</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Updated class for button style consistency after hero removal
    if st.button("LAUNCH ANALYST MODE", key="analyst", use_container_width=True):
        os.system("streamlit run app.py")

# Information Footer (Removed)