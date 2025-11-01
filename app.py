
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import google.generativeai as genai

# ---------------------------------------------------
# ⚙️ SETUP
# ---------------------------------------------------
st.set_page_config(page_title="⚡ Mumbai Electricity Bill Predictor", page_icon="💡", layout="centered")

# 💬 Configure Gemini API (replace with your real key)
genai.configure(api_key="AIzaSyBWVQfhoIbjRKelUfdI-SDNPGYdHOzyGso")

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# ---------------------------------------------------
# 🎨 STYLING
# ---------------------------------------------------
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #1f1f1f 0%, #343a40 100%);
        color: white;
        font-family: 'Poppins', sans-serif;
    }
    .title {
        font-size: 48px;
        font-weight: 800;
        color: #FFD700;
        text-align: center;
        margin-bottom: 0;
    }
    .subtitle {
        font-size: 18px;
        text-align: center;
        color: #DDDDDD;
        margin-top: 5px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #FFB800, #FF7300);
        color: black;
        font-weight: bold;
        border-radius: 12px;
        font-size: 18px;
        padding: 0.6em 1.2em;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #FFD700, #FF8C00);
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>💡 Mumbai Electricity Bill Predictor</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Smart AI-powered insights to save power ⚙️</div>", unsafe_allow_html=True)
st.markdown("---")

# ---------------------------------------------------
# 📥 USER INPUTS
# ---------------------------------------------------
num_rooms = st.slider("🏠 Number of Rooms", 1, 10, 3)
num_people = st.slider("👨‍👩‍👦 Number of People", 1, 15, 4)
avg_monthly_income = st.number_input("💰 Average Monthly Income (₹)", 10000, 300000, 75000)
total_kwh = st.slider("⚡ Total Monthly Consumption (kWh)", 50, 1000, 300)
provider = st.selectbox("🔌 Electricity Provider", ["BEST", "Tata Power", "MSEDCL"])

# Encode provider
provider_encoded = [0, 0, 0]
if provider == "BEST":
    provider_encoded = [1, 0, 0]
elif provider == "Tata Power":
    provider_encoded = [0, 1, 0]
else:
    provider_encoded = [0, 0, 1]

# ---------------------------------------------------
# 🔮 PREDICTION
# ---------------------------------------------------
if st.button("🔮 Predict My Bill!"):
    features = np.array([[num_rooms, num_people, avg_monthly_income,
                          provider_encoded[0], total_kwh,
                          provider_encoded[1], provider_encoded[2]]])
    prediction = model.predict(features)[0]

    st.subheader("💵 Estimated Monthly Bill:")
    st.success(f"₹ {prediction:.2f}")

    st.markdown("---")

    # ---------------------------------------------------
    # 🤖 GEMINI AI INSIGHTS
    # ---------------------------------------------------
    try:
        model_ai = genai.GenerativeModel("gemini-pro")
        prompt = f"""
        A Mumbai household has an estimated monthly electricity bill of ₹{prediction:.2f}.
        Suggest 5 realistic, smart, and locally practical ways to reduce their bill.
        Use emojis and simple bullet points for a friendly tone.
        """
        response = model_ai.generate_content(prompt)
        st.subheader("🤖 Watty’s Smart Energy Tips ⚡")
        st.write(response.text)

    except Exception as e:
        st.error(f"AI insights unavailable: {e}")

st.markdown("---")
st.caption("Made with ❤️ in Mumbai | Powered by Gemini AI ⚡")
