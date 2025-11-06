import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import time
import subprocess
import sys


# ------------------------------------------------------------
# ⚙️ CONFIGURATION
# ------------------------------------------------------------
st.set_page_config(
    page_title="Executive Analytics Platform - Beginner Mode",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Light Premium Color Palette - Clean Professional Theme
PRIMARY_BLUE = "#2C5F8D"       # Professional Blue
PRIMARY_LIGHT = "#E8F1F8"      # Light Blue Background
ACCENT_TEAL = "#1B7F79"        # Deep Teal
ACCENT_CORAL = "#D96846"       # Warm Coral
SURFACE_WHITE = "#FFFFFF"      # Pure White
SURFACE_GRAY = "#F5F7FA"       # Light Gray
TEXT_DARK = "#1A1A1A"          # Near Black
TEXT_MEDIUM = "#4A5568"        # Medium Gray
BORDER_LIGHT = "#D1D9E6"       # Light Border
SUCCESS = "#2F8F6E"            # Teal Green
WARNING = "#D97642"            # Orange
INFO = "#4A90A4"               # Blue Gray

# ------------------------------------------------------------
# 🎨 PREMIUM LIGHT STYLES
# ------------------------------------------------------------
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

/* Professional Headers */
h1 {{
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important;
    font-size: 3.2rem !important;
    color: {PRIMARY_BLUE} !important;
    letter-spacing: 1px;
    margin-bottom: 0.5rem !important;
    border-bottom: 3px solid {ACCENT_TEAL};
    padding-bottom: 12px;
}}

h2 {{
    font-family: 'Rajdhani', sans-serif !important;
    color: {PRIMARY_BLUE} !important;
    font-weight: 600 !important;
    font-size: 1.8rem !important;
    letter-spacing: 0.5px;
    margin-top: 2rem !important;
}}

h3 {{
    font-family: 'Rajdhani', sans-serif !important;
    color: {TEXT_MEDIUM} !important;
    font-weight: 500 !important;
    font-size: 1.2rem !important;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}}

h4 {{
    font-family: 'Rajdhani', sans-serif !important;
    color: {ACCENT_TEAL} !important;
    font-weight: 600 !important;
}}

/* Clean Metric Cards */
div.metric-card {{
    background: {SURFACE_WHITE};
    border-radius: 12px;
    padding: 32px;
    margin-bottom: 20px;
    box-shadow: 0 2px 12px rgba(44, 95, 141, 0.08);
    border: 1px solid {BORDER_LIGHT};
    border-left: 4px solid {ACCENT_TEAL};
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}

div.metric-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(44, 95, 141, 0.15);
    border-left: 4px solid {PRIMARY_BLUE};
}}

.metric-label {{
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.95rem;
    font-weight: 600;
    color: {TEXT_MEDIUM};
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 16px;
}}

.metric-value {{
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 2.4rem; /* Adjusted for safety with large numbers */
    font-weight: 700;
    color: {PRIMARY_BLUE};
    letter-spacing: -0.5px;
    line-height: 1;
    overflow: hidden;
    text-overflow: ellipsis;
}}

.metric-unit {{
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.1rem;
    color: {ACCENT_TEAL};
    font-weight: 500;
    margin-left: 6px;
}}

/* Client Portfolio Cards */
div.client-card {{
    background: {SURFACE_WHITE};
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 20px;
    border: 2px solid {BORDER_LIGHT};
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}}

div.client-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, {ACCENT_TEAL}, {PRIMARY_BLUE});
    transform: scaleX(0);
    transition: transform 0.3s ease;
}}

div.client-card:hover::before {{
    transform: scaleX(1);
}}

div.client-card:hover {{
    transform: translateY(-6px);
    box-shadow: 0 12px 32px rgba(44, 95, 141, 0.15);
    border: 2px solid {PRIMARY_BLUE};
}}

.client-id {{
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.6rem;
    font-weight: 700;
    color: {PRIMARY_BLUE};
    margin-bottom: 12px;
    letter-spacing: 0.5px;
}}

.rank-badge {{
    display: inline-block;
    padding: 6px 18px;
    border-radius: 6px;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin-bottom: 16px;
    text-transform: uppercase;
}}

.rank-tier1 {{
    background: linear-gradient(135deg, {ACCENT_TEAL}, {PRIMARY_BLUE});
    color: {SURFACE_WHITE};
}}

.rank-tier2 {{
    background: {PRIMARY_BLUE};
    color: {SURFACE_WHITE};
}}

.rank-tier3 {{
    background: {ACCENT_CORAL};
    color: {SURFACE_WHITE};
}}

.rank-tier4 {{
    background: {SURFACE_GRAY};
    color: {TEXT_DARK};
    border: 1px solid {BORDER_LIGHT};
}}

.client-detail {{
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.05rem;
    color: {TEXT_DARK};
    margin: 10px 0;
    font-weight: 400;
    line-height: 1.6;
}}

.client-detail strong {{
    color: {ACCENT_TEAL};
    font-weight: 600;
}}

/* Sidebar Professional Styling */
section[data-testid="stSidebar"] {{
    background: {SURFACE_WHITE};
    border-right: 2px solid {BORDER_LIGHT};
}}

section[data-testid="stSidebar"] * {{
    font-family: 'Rajdhani', sans-serif !important;
}}

/* Updated Sidebar Title H1 to remove emoji and keep styling */
section[data-testid="stSidebar"] h1 {{
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    color: {PRIMARY_BLUE} !important;
    border-bottom: 2px solid {ACCENT_TEAL};
    padding-bottom: 8px;
}}

section[data-testid="stSidebar"] h3 {{
    color: {TEXT_MEDIUM} !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
}}

/* Radio Navigation */
.stRadio > label {{
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: {TEXT_DARK} !important;
    letter-spacing: 0.5px !important;
}}

.stRadio > div > label > div {{
    background: {SURFACE_GRAY};
    padding: 12px 16px;
    margin: 6px 0;
    border-radius: 8px;
    transition: all 0.2s ease;
    border-left: 3px solid transparent;
}}

.stRadio > div > label > div:hover {{
    background: {PRIMARY_LIGHT};
    border-left: 3px solid {ACCENT_TEAL};
}}

/* Professional Buttons */
.stButton > button {{
    font-family: 'Rajdhani', sans-serif !important;
    background: {PRIMARY_BLUE};
    color: {SURFACE_WHITE};
    border: none;
    padding: 12px 28px;
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    border-radius: 6px;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(44, 95, 141, 0.2);
}}

.stButton > button:hover {{
    background: {ACCENT_TEAL};
    box-shadow: 0 4px 16px rgba(27, 127, 121, 0.3);
    transform: translateY(-2px);
}}

/* Professional Alert Boxes */
.alert-success {{
    background: linear-gradient(135deg, rgba(47, 143, 110, 0.08) 0%, rgba(47, 143, 110, 0.03) 100%);
    border-left: 4px solid {SUCCESS};
    padding: 20px 24px;
    border-radius: 8px;
    color: {TEXT_DARK};
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.05rem;
    font-weight: 500;
    margin: 20px 0;
    line-height: 1.7;
}}

.alert-warning {{
    background: linear-gradient(135deg, rgba(217, 118, 66, 0.08) 0%, rgba(217, 118, 66, 0.03) 100%);
    border-left: 4px solid {WARNING};
    padding: 20px 24px;
    border-radius: 8px;
    color: {TEXT_DARK};
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.05rem;
    font-weight: 500;
    margin: 20px 0;
    line-height: 1.7;
}}

.alert-info {{
    background: linear-gradient(135deg, rgba(74, 144, 164, 0.08) 0%, rgba(74, 144, 164, 0.03) 100%);
    border-left: 4px solid {INFO};
    padding: 20px 24px;
    border-radius: 8px;
    color: {TEXT_DARK};
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.05rem;
    font-weight: 500;
    margin: 20px 0;
    line-height: 1.7;
}}

/* Clean Dividers */
hr {{
    border: none;
    height: 2px;
    background: linear-gradient(90deg, transparent, {BORDER_LIGHT}, transparent);
    margin: 36px 0;
}}

/* Typography */
p, span, div:not(.metric-value):not(.metric-label) {{
    font-family: 'Rajdhani', sans-serif !important;
    color: {TEXT_DARK};
    font-size: 1.05rem;
    line-height: 1.7;
}}

/* Data Display Elements */
.stDataFrame {{
    font-family: 'Rajdhani', sans-serif !important;
}}

/* Spinner */
.stSpinner > div {{
    border-top-color: {PRIMARY_BLUE} !important;
}}

/* Section Container */
.section-container {{
    background: {SURFACE_WHITE};
    border-radius: 12px;
    padding: 28px;
    margin: 20px 0;
    box-shadow: 0 2px 12px rgba(44, 95, 141, 0.08);
    border: 1px solid {BORDER_LIGHT};
}}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 🧭 SIDEBAR NAVIGATION (MODIFIED)
# ------------------------------------------------------------
# Removed Emoji
st.sidebar.title("BEGINNER MODE")
st.sidebar.markdown("### INTELLIGENCE PLATFORM")
st.sidebar.markdown("Current Mode: **Beginner**")

# Updated switch label and target file

if st.sidebar.button("Switch to Business Mode"):
    st.query_params["mode"] = "analyst"
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", "app.py"])
    st.stop()

st.sidebar.markdown("---")

# ------------------------------------------------------------
# 📦 LOAD DATA
# ------------------------------------------------------------
@st.cache_data
def load_data():
    with st.spinner('LOADING DATA SOURCES'):
        time.sleep(1.0)
        
        if os.path.exists("data/OnlineRetail.csv"):
            raw = pd.read_csv("data/OnlineRetail.csv", encoding='latin1')
            raw["Total"] = raw["Quantity"] * raw["UnitPrice"]
            df = raw.dropna(subset=["CustomerID"]).groupby("CustomerID").agg(
                TotalSpend=("Total", "sum"),
                NumOrders=("InvoiceNo", "nunique"),
                Country=("Country", "first")
            ).reset_index()
            df["AOV"] = df["TotalSpend"] / df["NumOrders"]
            np.random.seed(42) 
            df["ConversionRate"] = np.random.uniform(2.5, 9.5, len(df))
            return df
        else:
            st.error("DATA SOURCE ERROR: OnlineRetail.csv NOT FOUND IN data/ DIRECTORY")
            st.stop()

df = load_data()

# ------------------------------------------------------------
# 🌍 PAGE NAVIGATION
# ------------------------------------------------------------
page = st.sidebar.radio("NAVIGATION", [
    "Performance Dashboard",
    "Client Analytics",
    "Product Intelligence"
])

# ------------------------------------------------------------
# 📊 PERFORMANCE DASHBOARD
# ------------------------------------------------------------
if page == "Performance Dashboard":
    st.title("PERFORMANCE DASHBOARD")
    st.markdown("### EXECUTIVE METRICS OVERVIEW")

    total_customers = len(df)
    avg_aov = df["AOV"].mean()
    avg_conversion = df["ConversionRate"].mean()
    total_revenue = df["TotalSpend"].sum()

    col1, col2, col3, col4 = st.columns(4)
    
    def metric_card(label, value, unit=""):
        return f"""
        <div class='metric-card'>
            <div class='metric-label'>{label}</div>
            <div style='display: flex; align-items: baseline;'>
                <span class='metric-value'>{value}</span>
                <span class='metric-unit'>{unit}</span>
            </div>
        </div>
        """

    with col1:
        st.markdown(metric_card("TOTAL CLIENTS", f"{total_customers:,}"), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card("TOTAL REVENUE", f"${total_revenue:,.0f}"), unsafe_allow_html=True)
    with col3:
        st.markdown(metric_card("AVG ORDER VALUE", f"${avg_aov:,.2f}"), unsafe_allow_html=True)
    with col4:
        st.markdown(metric_card("CONVERSION RATE", f"{avg_conversion:.2f}", "%"), unsafe_allow_html=True)

    st.markdown("---")
    
    # Strategic Analysis Section
    st.markdown("<div class='section-container'>", unsafe_allow_html=True)
    st.subheader("STRATEGIC ANALYSIS")
    
    if avg_aov > 300:
        st.markdown("<div class='alert-success'><strong>PREMIUM PERFORMANCE:</strong> Average order value exceeds $300, indicating strong customer value optimization. Current pricing and product mix strategies are delivering superior results. Continue monitoring high-value customer segments for expansion opportunities.</div>", unsafe_allow_html=True)
    elif avg_aov > 100:
        st.markdown("<div class='alert-info'><strong>STABLE METRICS:</strong> Average order value is within acceptable ranges at ${:,.2f}. Consider implementing targeted upselling campaigns and product bundling strategies to drive incremental growth in customer transaction values.</div>".format(avg_aov), unsafe_allow_html=True)
    else:
        st.markdown("<div class='alert-warning'><strong>ACTION REQUIRED:</strong> Average order value is below target thresholds. Immediate strategic review recommended for pricing structures, product offerings, and bundling opportunities to improve per-transaction revenue.</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Top Product Analysis
    if os.path.exists("data/OnlineRetail.csv"):
        raw = pd.read_csv("data/OnlineRetail.csv", encoding='latin1')
        raw["Total"] = raw["Quantity"] * raw["UnitPrice"]
        top_product = raw.groupby("Description")["Total"].sum().sort_values(ascending=False).head(1).index[0]
        top_product_revenue = raw.groupby("Description")["Total"].sum().sort_values(ascending=False).head(1).values[0]
        
        st.markdown("<div class='section-container'>", unsafe_allow_html=True)
        st.subheader("KEY REVENUE DRIVER")
        st.markdown(f"<div class='alert-info'><strong>PRIMARY ASSET:</strong> {top_product}<br><strong>REVENUE CONTRIBUTION:</strong> ${top_product_revenue:,.2f}<br><br>This product represents the highest revenue generator in the portfolio. Priority resource allocation recommended for inventory management, promotional support, and supply chain optimization to maintain revenue continuity.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# CLIENT ANALYTICS
# ------------------------------------------------------------
elif page == "Client Analytics":
    st.title("CLIENT ANALYTICS")
    st.markdown("### HIGH VALUE CUSTOMER PORTFOLIO")

    top_customers = df.sort_values("NumOrders", ascending=False).head(5).reset_index(drop=True)

    cols = st.columns(5)
    tiers = [
        ("TIER ONE", "rank-tier1"),
        ("TIER TWO", "rank-tier2"),
        ("TIER THREE", "rank-tier3"),
        ("PRIORITY", "rank-tier4"),
        ("STRATEGIC", "rank-tier4")
    ]
    
    for i, col in enumerate(cols):
        if i < len(top_customers):
            row = top_customers.iloc[i]
            tier_text, tier_class = tiers[i]
            
            col.markdown(f"""
                <div class='client-card'>
                    <div class='client-id'>CLIENT {int(row.CustomerID)}</div>
                    <div class='rank-badge {tier_class}'>{tier_text}</div>
                    <div class='client-detail'><strong>LOCATION:</strong> {row.Country}</div>
                    <div class='client-detail'><strong>TRANSACTIONS:</strong> {int(row.NumOrders)}</div>
                    <div class='client-detail'><strong>LIFETIME VALUE:</strong> ${row.TotalSpend:,.2f}</div>
                    <div class='client-detail'><strong>AVG ORDER:</strong> ${row.AOV:,.2f}</div>
                    <div class='client-detail'><strong>CONVERSION:</strong> {row.ConversionRate:.2f}%</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    
    st.markdown("<div class='section-container'>", unsafe_allow_html=True)
    st.subheader("CUSTOMER RETENTION STRATEGY")
    st.markdown("<div class='alert-success'><strong>PRIORITY ENGAGEMENT PROTOCOL:</strong> These high-value accounts represent the top 5 customers by transaction volume. Implement personalized engagement strategies including:<br><br>• Dedicated account management and priority support<br>• Exclusive promotional offers and early access programs<br>• Regular business reviews and strategic planning sessions<br>• Customized product recommendations based on purchase history<br><br>Maintaining strong relationships with these accounts is critical for sustained revenue growth and customer lifetime value optimization.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ------------------------------------------------------------
# PRODUCT INTELLIGENCE
# ------------------------------------------------------------
elif page == "Product Intelligence":
    st.title("PRODUCT INTELLIGENCE")
    st.markdown("### REVENUE ANALYSIS AND RISK ASSESSMENT")

    if os.path.exists("data/OnlineRetail.csv"):
        raw = pd.read_csv("data/OnlineRetail.csv", encoding='latin1')
        raw["Total"] = raw["Quantity"] * raw["UnitPrice"]

        # Top Products
        st.subheader("TOP REVENUE GENERATING PRODUCTS")
        top_products = raw.groupby("Description")["Total"].sum().nlargest(10).reset_index()
        
        fig1 = go.Figure(go.Bar(
            x=top_products["Total"],
            y=top_products["Description"],
            orientation='h',
            marker=dict(
                color=top_products["Total"],
                colorscale=[[0, PRIMARY_BLUE], [0.5, ACCENT_TEAL], [1, ACCENT_CORAL]],
                line=dict(color=BORDER_LIGHT, width=1)
            ),
            text=top_products["Total"].apply(lambda x: f'${x:,.0f}'),
            textposition='auto',
            textfont=dict(family='Rajdhani', size=12, color=TEXT_DARK),
            hovertemplate='<b>%{y}</b><br>Revenue: $%{x:,.2f}<extra></extra>'
        ))
        
        fig1.update_layout(
            xaxis_title="TOTAL REVENUE (USD)",
            yaxis_title="PRODUCT DESCRIPTION",
            template="plotly_white",
            paper_bgcolor=SURFACE_WHITE,
            plot_bgcolor=SURFACE_GRAY,
            font=dict(family='Rajdhani, sans-serif', color=TEXT_DARK, size=13),
            height=550,
            xaxis=dict(gridcolor=BORDER_LIGHT, showgrid=True),
            yaxis=dict(
                gridcolor=BORDER_LIGHT, 
                showgrid=False, 
                automargin=True,
                tickfont=dict(color=TEXT_DARK) 
            ),
            margin=dict(l=150, r=20, t=40, b=20)
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        st.markdown("---")

        # Return Risk Analysis
        st.subheader("PRODUCT RETURN ANALYSIS")
        returns = raw[raw["InvoiceNo"].astype(str).str.startswith("C")]
        
        if not returns.empty:
            returned = returns.groupby("Description")["Quantity"].sum().abs().nlargest(10).reset_index()
            
            fig2 = go.Figure(go.Bar(
                x=returned["Quantity"],
                y=returned["Description"],
                orientation='h',
                marker=dict(
                    color=returned["Quantity"],
                    colorscale=[[0, INFO], [0.5, WARNING], [1, ACCENT_CORAL]],
                    line=dict(color=BORDER_LIGHT, width=1)
                ),
                text=returned["Quantity"].apply(lambda x: f'{x:,.0f}'),
                textposition='auto',
                textfont=dict(family='Rajdhani', size=12, color=TEXT_DARK),
                hovertemplate='<b>%{y}</b><br>Returns: %{x:,}<extra></extra>'
            ))
            
            fig2.update_layout(
                xaxis_title="QUANTITY RETURNED (UNITS)",
                yaxis_title="PRODUCT DESCRIPTION",
                template="plotly_white",
                paper_bgcolor=SURFACE_WHITE,
                plot_bgcolor=SURFACE_GRAY,
                font=dict(family='Rajdhani, sans-serif', color=TEXT_DARK, size=13),
                height=550,
                xaxis=dict(gridcolor=BORDER_LIGHT, showgrid=True),
                yaxis=dict(
                    gridcolor=BORDER_LIGHT, 
                    showgrid=False, 
                    automargin=True,
                    tickfont=dict(color=TEXT_DARK) 
                ),
                margin=dict(l=150, r=20, t=40, b=20)
            )
            st.plotly_chart(fig2, use_container_width=True)
            
            st.markdown("<div class='alert-warning'><strong>QUALITY CONTROL ALERT:</strong> Elevated return volumes detected across multiple product lines. Recommended actions include:<br><br>• Dedicated account management and priority support<br>• Exclusive promotional offers and early access programs<br>• Regular business reviews and strategic planning sessions<br>• Customized product recommendations based on purchase history<br><br>Addressing these return patterns is essential for improving customer satisfaction and reducing operational costs.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='alert-success'><strong>OPTIMAL PERFORMANCE:</strong> No significant return activity detected. Current product quality standards and customer satisfaction levels are meeting expectations.</div>", unsafe_allow_html=True)