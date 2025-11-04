import streamlit as st
from predict_helper import predict_one
import time

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Customer Purchase Predictor",
    page_icon="💼",
    layout="wide",
)

# ---- CUSTOM CSS ----
st.markdown("""
    <style>
    /* Background gradient */
    body {
        background: linear-gradient(135deg, #56ab2f, #a8e063);
        font-family: 'Poppins', sans-serif;
    }

    /* Center main container */
    .main {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        border-radius: 25px;
        padding: 40px;
        box-shadow: 0 8px 40px rgba(0, 0, 0, 0.25);
        margin-top: 50px;
        animation: fadeIn 1s ease-in-out;
    }

    h1 {
        text-align: center;
        color: white !important;
        font-size: 50px !important;
        margin-bottom: 10px;
        font-weight: 700;
        letter-spacing: 1px;
        text-shadow: 2px 2px 15px rgba(0,0,0,0.25);
    }

    p.subtitle {
        text-align: center;
        color: #f5f5f5;
        font-size: 18px;
        margin-bottom: 40px;
    }

    .stNumberInput label {
        color: #ffffffcc !important;
        font-weight: 500;
        font-size: 17px;
    }

    .stButton>button {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 14px 30px;
        font-weight: 600;
        font-size: 18px;
        width: 100%;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #00b09b, #96c93d);
        transform: translateY(-3px);
        box-shadow: 0 6px 25px rgba(0,0,0,0.35);
    }

    .result-box {
        margin-top: 50px;
        padding: 30px;
        border-radius: 18px;
        background: rgba(255, 255, 255, 0.2);
        color: white;
        text-align: center;
        animation: slideUp 1s ease;
        box-shadow: 0 0 20px rgba(255,255,255,0.15);
    }

    .result-title {
        font-size: 28px;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .result-prob {
        font-size: 20px;
        opacity: 0.9;
    }

    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(15px);}
        to {opacity: 1; transform: translateY(0);}
    }

    @keyframes slideUp {
        from {opacity: 0; transform: translateY(40px);}
        to {opacity: 1; transform: translateY(0);}
    }
    </style>
""", unsafe_allow_html=True)

# ---- HEADER ----
st.markdown("<h1>Customer Purchase Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Predict whether a customer will make a purchase next month based on key metrics</p>", unsafe_allow_html=True)

# ---- INPUT SECTION ----
with st.container():
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        recency = st.number_input("Recency (days since last purchase)", min_value=0, value=30, step=1)
    with col2:
        frequency = st.number_input("Frequency (number of purchases)", min_value=0, value=2, step=1)
    with col3:
        monetary = st.number_input("Monetary (total spend)", min_value=0.0, value=100.0, step=10.0)

# ---- PREDICTION BUTTON ----
col_center = st.columns([2, 1, 2])[1]
with col_center:
    predict_clicked = st.button("Predict Purchase Likelihood")

# ---- RESULT SECTION ----
if predict_clicked:
    with st.spinner("Analyzing customer data..."):
        time.sleep(1.5)  # adds a small suspense effect
        pred, prob = predict_one(recency, frequency, monetary)

    st.markdown("<div class='result-box'>", unsafe_allow_html=True)
    if pred == 1:
        st.markdown(f"<div class='result-title'>Will Purchase Next Month</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='result-title'>Won't Purchase Next Month</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='result-prob'>Probability of Purchase: {prob:.2%}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---- FOOTER ----
st.markdown("""
    <br><br>
    <hr style='border: 1px solid rgba(255,255,255,0.3);'>
    <p style='text-align: center; color: rgba(255,255,255,0.8); font-size: 14px;'>
        © 2025 Customer Insights Lab | Built with Streamlit
    </p>
""", unsafe_allow_html=True)
