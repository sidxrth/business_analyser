import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import os
import sys
import pycountry   # for ISO-3 country conversion

# ------------------------------------------------------------
# ✅ Ensure Python can find your src/ folder for imports
# ------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from data_processing import generate_feature_dataset

# ------------------------------------------------------------
# 🧠 Load or Generate Data Automatically
# ------------------------------------------------------------
@st.cache_data
def load_data():
    processed_path = "processed_customer_data.csv"

    # If processed file exists, load it
    if os.path.exists(processed_path):
        st.info("📄 Loading existing processed data...")
        df = pd.read_csv(processed_path)
    else:
        # Otherwise, regenerate from raw data
        st.warning("⚙️ Processed data not found — generating from OnlineRetail dataset...")
        data_path_xlsx = os.path.join("data", "OnlineRetail.xlsx")
        data_path_csv = os.path.join("data", "OnlineRetail.csv")

        if os.path.exists(data_path_xlsx):
            df = generate_feature_dataset(data_path_xlsx)
        elif os.path.exists(data_path_csv):
            df = generate_feature_dataset(data_path_csv)
        else:
            st.error("❌ No OnlineRetail dataset found in /data folder!")
            st.stop()

    return df


# Load processed data
df = load_data()

# ------------------------------------------------------------
# 🎨 Streamlit Page Setup
# ------------------------------------------------------------
st.set_page_config(page_title="Business Analyzer Dashboard", layout="wide")
st.title("📊 Business Analyzer — Customer Insights Dashboard")

st.write(
    "Welcome! This dashboard provides analytical insights from the OnlineRetail dataset, "
    "showing key customer behavior metrics and purchasing patterns."
)

# ------------------------------------------------------------
# 📄 View Raw Data (First 50 Rows)
# ------------------------------------------------------------
st.subheader("📄 View First 50 Rows of Raw OnlineRetail Data")

data_path_xlsx = os.path.join("data", "OnlineRetail.xlsx")
data_path_csv = os.path.join("data", "OnlineRetail.csv")

if os.path.exists(data_path_xlsx):
    raw_df = pd.read_excel(data_path_xlsx, dtype={'StockCode': str}).head(50)
elif os.path.exists(data_path_csv):
    raw_df = pd.read_csv(data_path_csv, encoding='latin1', dtype={'StockCode': str}).head(50)
else:
    raw_df = None

if raw_df is not None:
    st.dataframe(raw_df)
else:
    st.warning("⚠️ Raw dataset not found in the /data folder.")

# ------------------------------------------------------------
# 📈 KPI Metrics Section
# ------------------------------------------------------------
st.subheader("📈 Key Customer Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("Average Order Value (AOV)", f"${df['AOV'].mean():.2f}")
col2.metric("Return Rate", f"{df['ReturnRate'].mean():.2f}%")
col3.metric("Average Basket Size", f"{df['AvgBasketSize'].mean():.2f}")

col4, col5, col6 = st.columns(3)
col4.metric("Unique Products Purchased", f"{df['UniqueProducts'].mean():.0f}")
col5.metric("Customer Tenure (Days)", f"{df['CustomerTenure'].mean():.0f}")
col6.metric("Purchase Interval (Days)", f"{df['PurchaseInterval'].mean():.1f}")

# ------------------------------------------------------------
# 📊 Feature Distributions
# ------------------------------------------------------------
st.subheader("📊 Feature Distributions")

# AOV Distribution
fig, ax = plt.subplots()
ax.hist(df['AOV'], bins=20, color='green', alpha=0.7)
ax.set_title("Distribution of Average Order Value (AOV)")
ax.set_xlabel("AOV ($)")
ax.set_ylabel("Customer Count")
st.pyplot(fig)

# Customer Tenure Distribution
fig, ax = plt.subplots()
ax.hist(df['CustomerTenure'], bins=20, color='orange', alpha=0.7)
ax.set_title("Distribution of Customer Tenure")
ax.set_xlabel("Days as Customer")
ax.set_ylabel("Count")
st.pyplot(fig)

# ------------------------------------------------------------
# 🌍 Country-Wise AOV Map (ISO-3 compatible)
# ------------------------------------------------------------
st.subheader("🌍 Average Order Value by Country")

if 'Country' in df.columns:
    def get_iso3(country_name):
        try:
            return pycountry.countries.lookup(country_name).alpha_3
        except:
            return None

    df['Country_ISO'] = df['Country'].apply(get_iso3)
    df = df.dropna(subset=['Country_ISO'])

    fig_map = px.choropleth(
        df,
        locations="Country_ISO",
        color="AOV",
        title="Average Order Value by Country (ISO-3)",
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_map, width='stretch')
else:
    st.warning("⚠️ 'Country' column not found in dataset.")

# ------------------------------------------------------------
# 💰 Simplified Relationship Between Last Month Spend and AOV
# ------------------------------------------------------------
if 'LastMonthSpend' in df.columns:
    st.subheader("💰 How Spending Affects Average Order Value (Simplified)")

    bins = [0, 200, 400, 600, 800, 1000]
    labels = ["0–200", "200–400", "400–600", "600–800", "800–1000"]
    df['SpendRange'] = pd.cut(df['LastMonthSpend'], bins=bins, labels=labels, include_lowest=True)

    # Explicitly set observed=False to silence future warnings
    spend_summary = df.groupby('SpendRange', observed=False)['AOV'].mean().reset_index()

    fig, ax = plt.subplots()
    ax.bar(spend_summary['SpendRange'], spend_summary['AOV'], color='teal', alpha=0.85)
    ax.set_title("Average Order Value by Spending Range")
    ax.set_xlabel("Last Month Spend Range ($)")
    ax.set_ylabel("Average Order Value ($)")
    st.pyplot(fig)

# ------------------------------------------------------------
# 🧠 Optional ML Insights (if available)
# ------------------------------------------------------------
if 'PredictedSegment' in df.columns:
    st.subheader("🧩 Customer Segmentation Results")
    segment_counts = df['PredictedSegment'].value_counts()
    st.bar_chart(segment_counts)

if 'ChurnProb' in df.columns:
    st.subheader("⚠️ High-Risk (Churn) Customers")
    high_risk = df[df['ChurnProb'] > 0.8]
    st.write(f"Number of high-risk customers: **{len(high_risk)}**")
    st.dataframe(high_risk[['CustomerID', 'ChurnProb', 'AOV', 'ReturnRate']])

# ------------------------------------------------------------
# 📂 Data Preview Section
# ------------------------------------------------------------
with st.expander("📄 View Processed Data (first 10 rows)"):
    st.dataframe(df.head(10))

st.success("✅ Dashboard loaded successfully!")
