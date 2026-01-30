import streamlit as st
import pandas as pd
from datagen import stream_data
from riskmode import predict_risk

st.set_page_config(page_title="Remote Patient Monitoring", layout="wide")

st.title("🏥 Remote Patient Monitoring Dashboard")
st.markdown("Live monitoring of patient vitals with AI risk prediction")

# Session state
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame()

# Sidebar controls
st.sidebar.header("Controls")
num_patients = st.sidebar.slider("Number of Patients", 1, 10, 5)
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 1, 5, 2)

# Generate new data
new_data = stream_data(num_patients)
new_data["Risk Level"] = new_data.apply(predict_risk, axis=1)

# Append history
st.session_state.data = pd.concat(
    [st.session_state.data, new_data]
).tail(300)

st.session_state.data["timestamp"] = pd.to_datetime(
    st.session_state.data["timestamp"]
)

# Auto-refresh (SAFE WAY)
st.experimental_autorefresh(interval=refresh_rate * 1000, key="refresh")

# ---- UI ----
st.subheader("📊 Live Patient Vitals")
st.dataframe(new_data, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("❤️ Heart Rate Trend")
    hr_df = st.session_state.data.pivot_table(
        index="timestamp",
        columns="patient_id",
        values="heart_rate",
        aggfunc="mean"
    )
    st.line_chart(hr_df)

with col2:
    st.subheader("🫁 SpO₂ Trend")
    spo2_df = st.session_state.data.pivot_table(
        index="timestamp",
        columns="patient_id",
        values="spo2",
        aggfunc="mean"
    )
    st.line_chart(spo2_df)

# Alerts
st.subheader("🚨 Alerts")
alerts = new_data[new_data["Risk Level"] == "High Risk"]

if not alerts.empty:
    st.error("⚠ CRITICAL PATIENT ALERTS!")
    st.dataframe(alerts, use_container_width=True)
else:
    st.success("All patients stable ✅")

