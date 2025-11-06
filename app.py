import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import warnings
from datetime import datetime
import subprocess
import sys


warnings.filterwarnings("ignore", message="Please replace `use_container_width`", category=UserWarning)

# ------------------------------------------------------------
# ⚙️ CONFIGURATION & COLOR PALETTE
# ------------------------------------------------------------
st.set_page_config(page_title="Business Analyzer – Business Mode", layout="wide")

# Light Premium Color Palette - Clean Professional Theme
PRIMARY_BLUE = "#2C5F8D"
PRIMARY_LIGHT = "#E8F1F8"
ACCENT_TEAL = "#1B7F79"
ACCENT_CORAL = "#D96846"
SURFACE_WHITE = "#FFFFFF"
SURFACE_GRAY = "#F5F7FA"
TEXT_DARK = "#1A1A1A"
TEXT_MEDIUM = "#4A5568"
BORDER_LIGHT = "#D1D9E6"
SUCCESS = "#2F8F6E"
WARNING = "#D97642"
INFO = "#4A90A4"

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

/* 💅 ST.SELECTBOX STYLING (FOR RECOMMENDATIONS PAGE) */
/* Label */
.stSelectbox > label {{
    font-family: 'Rajdhani', sans-serif !important;
    color: {TEXT_DARK} !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    letter-spacing: 0.5px !important;
}}

/* Main box (selected item) */
div[data-baseweb="select"] > div {{
    background-color: {SURFACE_WHITE} !important;
    border: 1px solid {BORDER_LIGHT} !important;
    border-radius: 6px !important;
}}

/* Text inside the main box (selected value) */
div[data-baseweb="select"] div[data-testid="stMarkdownContainer"] {{
    font-family: 'Rajdhani', sans-serif !important;
    color: {TEXT_DARK} !important;
}}
/* This targets the placeholder text too */
div[data-baseweb="select"] > div > div {{
    font-family: 'Rajdhani', sans-serif !important;
    color: {TEXT_DARK} !important;
}}


/* 🌟🌟🌟 FINAL FIX (TYPO CORRECTED + MORE AGGRESSIVE) 🌟🌟🌟 */
/* Dropdown list (the pop-up menu) */
div[data-baseweb="popover"] ul[role="listbox"] {{
     background-color: #0E1117 !important;  /* Dark background for the list */
     border: 1px solid {BORDER_LIGHT} !important;
}}

/* Dropdown items (the options) */
div[data-baseweb="popover"] ul[role="listbox"] li {{
    font-family: 'Rajdhani', sans-serif !important;
    background-color: #0E1117 !important; /* Dark background */
    color: white !important; /* 👈 APPLY TO LI ITSELF */
}}

/* Force text color on all elements *inside* the list item */
div[data-baseweb="popover"] ul[role="listbox"] li * {{
    color: white !important; /* 👈 FORCE ON ALL CHILDREN */
    font-family: 'Rajdhani', sans-serif !important;
}}

/* Dropdown items on hover */
div[data-baseweb="popover"] ul[role="listbox"] li:hover {{
    background-color: {PRIMARY_BLUE} !important; /* Use your theme color for hover */
    color: white !important; /* 👈 APPLY TO LI ON HOVER */
}}

/* Force text color on hover (TYPO FIXED HERE) */
div[data-baseweb="popover"] ul[role="listbox"] li:hover * {{
    color: white !important; /* 👈 FORCE ON CHILDREN ON HOVER */
    background-color: transparent !important; /* Prevent child background override */
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
    st.query_params["mode"] = "beginner"
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", "simple_app.py"])
    st.stop()
st.sidebar.markdown("---")

# ------------------------------------------------------------
# DATA LOADING
# ------------------------------------------------------------
# ------------------------------------------------------------
# DATA LOADING
# ------------------------------------------------------------
@st.cache_data(ttl=3600, max_entries=1)
def load_data():
    processed_file = "processed_customer_data.csv"
    raw_file = "data/OnlineRetail.csv"  # <-- This path is correct as per your info

    if os.path.exists(processed_file):
        try:
            # Try to read the processed file
            st.info(f"Loading cached data from {processed_file}...")
            return pd.read_csv(processed_file)
        except pd.errors.EmptyDataError:
            # If it's empty or corrupt, delete it and proceed
            st.warning("Found empty processed file. Deleting and reprocessing.")
            os.remove(processed_file)

    # Check for the raw file
    if os.path.exists(raw_file): 
        st.info("Processing raw data... This may take a moment.")
        
        df = pd.read_csv(raw_file, encoding='latin1')
        
        # --- Improved AOV Logic ---
        # 1. Clean data: drop rows without CustomerID
        df = df.dropna(subset=["CustomerID"])
        
        # 2. Filter for *sales transactions only* (positive quantity and price)
        df_sales = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)].copy()
        
        if df_sales.empty:
            st.error("No valid sales data found after filtering. Cannot calculate AOV.")
            st.stop()
            
        # 3. Calculate TotalSpend on sales data
        df_sales["TotalSpend"] = df_sales["Quantity"] * df_sales["UnitPrice"]

        # 4. Aggregate order counts and spend from sales data
        order_counts = df_sales.groupby("CustomerID")["InvoiceNo"].nunique().reset_index(name="NumOrders")
        customer_spend = df_sales.groupby("CustomerID").agg(
            TotalSpend=('TotalSpend', 'sum'),
            Country=('Country', 'first') # Keep country
        ).reset_index()

        # 5. Merge into a final customer dataframe
        customer_df = customer_spend.merge(order_counts, on="CustomerID", how="left")
        
        # 6. Calculate AOV
        # Ensure NumOrders is not zero to avoid division by zero
        customer_df = customer_df[customer_df["NumOrders"] > 0]
        customer_df["AOV"] = customer_df["TotalSpend"] / customer_df["NumOrders"]
        # --- End Improved Logic ---

        # Add simulated ReturnRate
        np.random.seed(43) 
        customer_df["ReturnRate"] = np.random.uniform(1, 10, len(customer_df))
        
        # Save the new processed file and return
        try:
            customer_df.to_csv(processed_file, index=False)
            st.success("Data processing complete! Saved to processed_customer_data.csv")
        except Exception as e:
            st.error(f"Failed to save processed file: {e}")
            
        return customer_df
    
    else:
        # This error is now correct
        st.error(f"Dataset not found. Please place 'OnlineRetail.csv' in the /data folder.")
        st.stop()

df = load_data()


# ------------------------------------------------------------
# SIDEBAR NAVIGATION (MODIFIED)
# ------------------------------------------------------------
page = st.sidebar.radio("CHOOSE A SECTION", [
    "Overview",
    "RFM Analysis",
    "Product & Revenue Insights",
    "Regional Performance",
    "Fraud & Anomaly Detection",
    "Alerts & Notifications"
    # 👈 Recommendations & AI Query Assistant removed
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
            return pd.Series([labels[0]]* len(series), index=series.index)

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
# ------------------------------------------------------------
# FRAUD & ANOMALY DETECTION (WORKING VERSION)
# ------------------------------------------------------------
elif page == "Fraud & Anomaly Detection":
    st.title("FRAUD & ANOMALY DETECTION")
    st.markdown("### Detect unusual transactions and outlier purchase patterns.")
    st.markdown(f"<div class='section-container'>", unsafe_allow_html=True)

    if os.path.exists("data/OnlineRetail.csv"):
        raw = pd.read_csv("data/OnlineRetail.csv", encoding='latin1')
        raw["Total"] = raw["Quantity"] * raw["UnitPrice"]

        # Basic rule-based anomaly detection
        anomalies = raw[(raw["Total"] < 0) | (raw["Total"] > raw["Total"].mean() * 5)]

        st.warning(f"{len(anomalies)} potential anomalies detected.")
        st.dataframe(anomalies[["InvoiceNo", "StockCode", "Quantity", "UnitPrice", "Total"]], use_container_width=True)

        if not anomalies.empty:
            fig = px.scatter(
                anomalies, x="Quantity", y="Total",
                color="UnitPrice", title="Anomalous Transactions Overview",
                hover_data=["InvoiceNo", "StockCode"]
            )
            fig.update_layout(
                paper_bgcolor=SURFACE_WHITE,
                plot_bgcolor=SURFACE_GRAY,
                font=dict(family='Rajdhani, sans-serif', color=TEXT_DARK),
                margin=dict(l=40, r=20, t=60, b=40)
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Dataset not found. Please add OnlineRetail.csv in the /data folder.")

    st.markdown("</div>", unsafe_allow_html=True)


# ------------------------------------------------------------
# ALERTS & NOTIFICATIONS (WORKING VERSION)
# ------------------------------------------------------------
elif page == "Alerts & Notifications":
    st.title("🚨 ALERTS & NOTIFICATIONS")
    st.markdown("### Detect sudden changes in revenue or order trends.")
    st.markdown(f"<div class='section-container'>", unsafe_allow_html=True)

    if os.path.exists("data/OnlineRetail.csv"):
        # Use the cached raw data loader if possible, or define a local one
        @st.cache_data(ttl=3600)
        def load_raw_data_alerts(file_path):
            df = pd.read_csv(file_path, encoding='latin1')
            df["Total"] = df["Quantity"] * df["UnitPrice"]
            df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors='coerce')
            return df.dropna(subset=['InvoiceDate'])

        raw = load_raw_data_alerts("data/OnlineRetail.csv")

        daily_sales = raw.groupby(raw["InvoiceDate"].dt.date)["Total"].sum().reset_index()
        daily_sales["Change"] = daily_sales["Total"].pct_change() * 100

        # Define a dynamic threshold, e.g., 3 standard deviations from the mean change
        alert_threshold_high = daily_sales["Change"].mean() + (3 * daily_sales["Change"].std())
        alert_threshold_low = daily_sales["Change"].mean() - (3 * daily_sales["Change"].std())
        
        st.info(f"Alert thresholds set at: > {alert_threshold_high:.2f}% or < {alert_threshold_low:.2f}% change.")

        alerts = daily_sales[(daily_sales["Change"] > alert_threshold_high) | (daily_sales["Change"] < alert_threshold_low)]

        if not alerts.empty:
            st.error("⚠️ Sudden revenue changes detected:")
            st.dataframe(alerts, use_container_width=True)

            fig = px.line(daily_sales, x="InvoiceDate", y="Total", title="Daily Revenue Trend (with Alerts Highlighted)")
            fig.add_scatter(
                x=alerts["InvoiceDate"], y=alerts["Total"],
                mode="markers", marker=dict(color="red", size=10),
                name="Alert Points"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("✅ No major anomalies detected in recent sales.")
    else:
        st.error("Dataset not found. Please add OnlineRetail.csv in the /data folder.")

    st.markdown("</div>", unsafe_allow_html=True)
