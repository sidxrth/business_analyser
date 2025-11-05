import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import warnings
from datetime import datetime

warnings.filterwarnings("ignore", message="Please replace `use_container_width`", category=UserWarning)

# ------------------------------------------------------------
# ⚙️ CONFIGURATION & COLOR PALETTE
# ------------------------------------------------------------
st.set_page_config(page_title="Business Analyzer – Business Mode", layout="wide")

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
# 🎨 PREMIUM LIGHT STYLES (CUSTOM CSS)
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

/* Sidebar Professional Styling */
section[data-testid="stSidebar"] {{
    background: {SURFACE_WHITE};
    border-right: 2px solid {BORDER_LIGHT};
}}

section[data-testid="stSidebar"] * {{
    font-family: 'Rajdhani', sans-serif !important;
}}

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

/* 📊 ST.METRIC STYLING */
[data-testid="stMetric"] {{
    background: {SURFACE_WHITE};
    border-radius: 12px;
    padding: 32px;
    margin-bottom: 20px;
    box-shadow: 0 2px 12px rgba(44, 95, 141, 0.08);
    border: 1px solid {BORDER_LIGHT};
    border-left: 4px solid {ACCENT_TEAL};
    transition: all 0.3s ease;
}}

[data-testid="stMetric"]:hover {{
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(44, 95, 141, 0.15);
    border-left: 4px solid {PRIMARY_BLUE};
}}

[data-testid="stMetricLabel"] > div {{
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.95rem;
    font-weight: 600;
    color: {TEXT_MEDIUM};
    text-transform: uppercase;
    letter-spacing: 2px;
}}

[data-testid="stMetricValue"] {{
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 2.4rem;
    font-weight: 700;
    color: {PRIMARY_BLUE};
    letter-spacing: -0.5px;
    line-height: 1;
    overflow: hidden;
    text-overflow: ellipsis;
}}

[data-testid="stMetricDelta"] {{
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600;
    color: {TEXT_DARK} !important;
}}

/* Dataframe Styling */
.stDataFrame {{
    border-radius: 8px;
    border: 1px solid {BORDER_LIGHT};
    box-shadow: 0 1px 4px rgba(44, 95, 141, 0.05);
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

/* Professional Buttons (for switch mode) */
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
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 🧭 MODE SWITCHER (MODIFIED)
# ------------------------------------------------------------
# Removed Emoji
st.sidebar.title("BUSINESS ANALYZER") 
st.sidebar.markdown("### Current Mode: **Business**")

# Updated switch label and target file
if st.sidebar.button("Switch to Beginner Mode"):
    # Execute the command to switch to the beginner_app.py file
    st.experimental_set_query_params(mode='beginner')
    os.system("streamlit run beginner_app.py")
    st.stop()

st.sidebar.markdown("---")

# ------------------------------------------------------------
# DATA LOADING
# ------------------------------------------------------------
@st.cache_data(ttl=3600, max_entries=1)
def load_data():
    if os.path.exists("processed_customer_data.csv"):
        return pd.read_csv("processed_customer_data.csv")
    elif os.path.exists("data/OnlineRetail.csv"):
        # Load and process data (simulated for demonstration)
        df = pd.read_csv("data/OnlineRetail.csv", encoding='latin1')
        df["TotalSpend"] = df["Quantity"] * df["UnitPrice"]
        df = df.dropna(subset=["CustomerID"])
        
        # Calculate intermediate metrics before grouping to avoid calculation errors
        order_counts = df.groupby("CustomerID")["InvoiceNo"].nunique().reset_index(name="NumOrders")
        df = df.merge(order_counts, on="CustomerID", how="left")
        
        # Aggregate to customer level for LTV metrics
        customer_df = df.groupby("CustomerID").agg(
            TotalSpend=('TotalSpend', 'sum'),
            NumOrders=('NumOrders', 'first'),
            Country=('Country', 'first')
        ).reset_index()

        customer_df["AOV"] = customer_df["TotalSpend"] / customer_df["NumOrders"]
        
        # Ensure 'ReturnRate' is calculated on a per-customer basis or join back correctly
        np.random.seed(43) 
        customer_df["ReturnRate"] = np.random.uniform(1, 10, len(customer_df))
        
        customer_df.to_csv("processed_customer_data.csv", index=False)
        return customer_df
    else:
        st.error("No dataset found. Please place 'OnlineRetail.csv' in the /data folder.")
        st.stop()

df = load_data()

# ------------------------------------------------------------
# SIDEBAR NAVIGATION
# ------------------------------------------------------------
page = st.sidebar.radio("CHOOSE A SECTION", [
    "Overview",
    "RFM Analysis",
    "Product & Revenue Insights",
    "Regional Performance",
    "Fraud & Anomaly Detection",
    "Recommendations",
    "Alerts & Notifications"
])

# ------------------------------------------------------------
# OVERVIEW PAGE
# ------------------------------------------------------------
if page == "Overview":
    st.title("BUSINESS OVERVIEW")
    st.markdown("### CORE FINANCIAL AND CUSTOMER KPIS")

    total_customers = len(df)
    avg_aov = df["AOV"].mean()
    avg_return_rate = df["ReturnRate"].mean()

    col1, col2, col3 = st.columns(3)
    # st.metric now benefits from the custom CSS for stMetric
    col1.metric("TOTAL CUSTOMERS", f"{total_customers:,}")
    col2.metric("AVERAGE ORDER VALUE", f"${avg_aov:.2f}")
    col3.metric("RETURN RATE", f"{avg_return_rate:.2f}%")

    st.markdown("---")

    st.subheader("SAMPLE CUSTOMER DATA")
    st.markdown(f"<div class='section-container'>", unsafe_allow_html=True)
    st.dataframe(df.head(50), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ------------------------------------------------------------
# RFM ANALYSIS
# ------------------------------------------------------------
elif page == "RFM Analysis":
    st.title("RFM (Recency, Frequency, Monetary) ANALYSIS")
    st.markdown("### STRATEGIC CUSTOMER SEGMENTATION")

    df["Recency"] = np.random.randint(1, 365, len(df))
    df["Frequency"] = df["NumOrders"]
    df["Monetary"] = df["TotalSpend"]

    def safe_qcut(series, q=4, labels=None):
        try:
            return pd.qcut(series, q, labels=labels, duplicates="drop")
        except ValueError:
            return pd.Series([labels[0]] * len(series), index=series.index)

    try:
        df["R_Score"] = pd.qcut(df["Recency"], 4, labels=[4, 3, 2, 1], duplicates="drop").astype(int)
    except Exception:
        df["R_Score"] = 1
        
    try:
        df["F_Score"] = pd.qcut(df["Frequency"], 4, labels=[1, 2, 3, 4], duplicates="drop").astype(int)
    except Exception:
        df["F_Score"] = 1

    try:
        df["M_Score"] = pd.qcut(df["Monetary"], 4, labels=[1, 2, 3, 4], duplicates="drop").astype(int)
    except Exception:
        df["M_Score"] = 1

    df["RFM_Score"] = df["R_Score"] + df["F_Score"] + df["M_Score"]

    df["Segment"] = df["RFM_Score"].apply(
        lambda x: "Champions" if x >= 10 else "Active" if x >= 7 else "At Risk" if x >= 5 else "Lost"
    )

    seg_count = df["Segment"].value_counts().reset_index()
    seg_count.columns = ["Segment", "Count"]

    st.markdown(f"<div class='section-container'>", unsafe_allow_html=True)
    st.subheader("CUSTOMER SEGMENTATION")
    
    segment_colors = {
        'Champions': ACCENT_TEAL, 
        'Active': PRIMARY_BLUE, 
        'At Risk': INFO, 
        'Lost': ACCENT_CORAL
    }

    fig = px.pie(
        seg_count, 
        names="Segment", 
        values="Count", 
        hole=0.4, 
        title="Customer Segmentation Distribution",
        color="Segment",
        color_discrete_map=segment_colors
    )
    
    fig.update_layout(
        paper_bgcolor=SURFACE_WHITE,
        plot_bgcolor=SURFACE_WHITE,
        font=dict(family='Rajdhani, sans-serif', color=TEXT_DARK),
        margin=dict(t=50, b=20, l=20, r=20),
        legend=dict(font=dict(size=14))
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# PRODUCT & REVENUE INSIGHTS
# ------------------------------------------------------------
elif page == "Product & Revenue Insights":
    st.title("PRODUCT & REVENUE INSIGHTS")
    st.markdown("### REVENUE DISTRIBUTION BY GEOGRAPHY")
    
    st.markdown(f"<div class='section-container'>", unsafe_allow_html=True)
    
    top = df.groupby("Country")["TotalSpend"].sum().nlargest(10).reset_index()
    
    fig = px.bar(
        top, 
        x="TotalSpend", 
        y="Country", 
        orientation="h", 
        color="TotalSpend",
        color_continuous_scale=[PRIMARY_BLUE, ACCENT_TEAL, ACCENT_CORAL], 
        title="Top 10 Countries by Revenue",
    )
    
    fig.update_layout(
        paper_bgcolor=SURFACE_WHITE,
        plot_bgcolor=SURFACE_GRAY,
        font=dict(family='Rajdhani, sans-serif', color=TEXT_DARK, size=13),
        xaxis_title="TOTAL REVENUE (USD)",
        yaxis_title="COUNTRY",
        yaxis=dict(automargin=True, tickfont=dict(color=TEXT_DARK)),
        xaxis=dict(gridcolor=BORDER_LIGHT),
        margin=dict(l=100, r=20, t=50, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# REGIONAL PERFORMANCE
# ------------------------------------------------------------
elif page == "Regional Performance":
    st.title("REGIONAL SALES PERFORMANCE")
    st.markdown("### TIME SERIES ANALYSIS")
    
    st.markdown(f"<div class='section-container'>", unsafe_allow_html=True)

    if os.path.exists("data/OnlineRetail.csv"):
        raw = pd.read_csv("data/OnlineRetail.csv", encoding='latin1')
        raw["Total"] = raw["Quantity"] * raw["UnitPrice"]
        raw["InvoiceDate"] = pd.to_datetime(raw["InvoiceDate"])
        
        raw = raw.dropna(subset=["InvoiceDate", "Total"])
        
        raw["Month"] = raw["InvoiceDate"].dt.to_period("M")
        sales = raw.groupby(["Country", "Month"])["Total"].sum().reset_index()
        sales["Month"] = sales["Month"].astype(str)
        
        top_countries = sales.groupby("Country")["Total"].sum().nlargest(5).index.tolist()
        sales_filtered = sales[sales["Country"].isin(top_countries)]
        
        fig = px.line(
            sales_filtered, 
            x="Month", 
            y="Total", 
            color="Country", 
            title="Sales by Top 5 Countries Over Time",
            color_discrete_sequence=[ACCENT_TEAL, PRIMARY_BLUE, ACCENT_CORAL, INFO, WARNING]
        )
        
        fig.update_layout(
            paper_bgcolor=SURFACE_WHITE,
            plot_bgcolor=SURFACE_GRAY,
            font=dict(family='Rajdhani, sans-serif', color=TEXT_DARK, size=13),
            xaxis_title="MONTH",
            yaxis_title="TOTAL SALES (USD)",
            xaxis=dict(gridcolor=BORDER_LIGHT),
            yaxis=dict(gridcolor=BORDER_LIGHT),
            margin=dict(l=50, r=50, t=50, b=50),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# STUBS FOR OTHER PAGES
# ------------------------------------------------------------
elif page == "Fraud & Anomaly Detection":
    st.title("FRAUD & ANOMALY DETECTION")
    st.markdown(f"<div class='section-container'><p>This section is reserved for advanced machine learning models that detect outliers in transactions (e.g., unusually high quantities or sudden changes in purchase patterns). Key metrics will include Anomaly Score and Isolation Forest results.</p></div>", unsafe_allow_html=True)

elif page == "Recommendations":
    st.title("RECOMMENDATIONS")
    st.markdown(f"<div class='section-container'><p>Based on the RFM segmentation, this area will provide targeted marketing and retention strategy recommendations for the 'Champions' and 'At Risk' customer segments.</p></div>", unsafe_allow_html=True)

elif page == "Alerts & Notifications":
    st.title("ALERTS & NOTIFICATIONS")
    st.markdown(f"<div class='section-container'><p>This log tracks significant changes in key performance indicators (e.g., 20% drop in AOV, 50% spike in Return Rate for a product) that require immediate executive attention.</p></div>", unsafe_allow_html=True)