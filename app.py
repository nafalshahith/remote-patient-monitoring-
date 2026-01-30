import streamlit as st
import pandas as pd
from datagen import stream_data
from riskmode import predict_risk

# Page config
st.set_page_config(
    page_title="Remote Patient Monitoring",
    layout="wide"
)

# Header
st.title("🏥 Remote Patient Monitoring Dashboard")
st.markdown("Live monitoring of patient vitals with risk prediction")

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame()

# Sidebar controls
st.sidebar.header("Controls")
num_patients = st.sidebar.slider("Number of Patients", 1, 10, 5)
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 3, 10, 5)

# Generate ONE batch per refresh
new_data = stream_data(num_patients)
new_data["Risk Level"] = new_data.apply(predict_risk, axis=1)

# Append data safely
st.session_state.data = pd.concat(
    [st.session_state.data, new_data],
    ignore_index=True
).tail(300)

# Ensure timestamp
st.session_state.data["timestamp"] = pd.to_datetime(
    st.session_state.data["timestamp"]
)

# Auto refresh (cloud-safe)
st.experimental_autorefresh(
    interval=refresh_rate * 1000,
    key="refresh"
)

# ---- UI ----
st.subheader("📊 Live Patient Snapshot")
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
st.subheader("🚨 High-Risk Alerts")
alerts = new_data[new_data["Risk Level"] == "High Risk"]

if not alerts.empty:
    st.error("⚠ Critical patients detected!")
    st.dataframe(alerts, use_container_width=True)
else:
    st.success("All patients are stable ✅")
