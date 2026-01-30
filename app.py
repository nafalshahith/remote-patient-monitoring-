import streamlit as st
import pandas as pd
import time
from datagen import stream_data
from riskmode import predict_risk

st.set_page_config(page_title="Remote Patient Monitoring", layout="wide")

st.title("🏥 Remote Patient Monitoring Dashboard")
st.markdown("Simulated live patient vitals with risk assessment")

# Initialize state
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame()
if "last_run" not in st.session_state:
    st.session_state.last_run = 0.0

# Sidebar
st.sidebar.header("Controls")
num_patients = st.sidebar.slider("Number of Patients", 1, 10, 5)
refresh_rate = st.sidebar.slider("Refresh every (seconds)", 3, 10, 5)

# Controlled live simulation
current_time = time.time()

if current_time - st.session_state.last_run >= refresh_rate:
    new_data = stream_data(num_patients)
    new_data["Risk Level"] = new_data.apply(predict_risk, axis=1)

    st.session_state.data = pd.concat(
        [st.session_state.data, new_data],
        ignore_index=True
    ).tail(300)

    st.session_state.last_run = current_time

# UI rendering
if not st.session_state.data.empty:
    st.subheader("📊 Live Patient Snapshot")
    st.dataframe(
        st.session_state.data.tail(num_patients),
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("❤️ Heart Rate Trend")
        st.line_chart(
            st.session_state.data.pivot_table(
                index="timestamp",
                columns="patient_id",
                values="heart_rate",
                aggfunc="mean"
            )
        )

    with col2:
        st.subheader("🫁 SpO₂ Trend")
        st.line_chart(
            st.session_state.data.pivot_table(
                index="timestamp",
                columns="patient_id",
                values="spo2",
                aggfunc="mean"
            )
        )

    st.subheader("🚨 High-Risk Alerts")
    alerts = st.session_state.data[
        st.session_state.data["Risk Level"] == "High Risk"
    ]

    if not alerts.empty:
        st.error("Critical patients detected!")
        st.dataframe(alerts, use_container_width=True)
    else:
        st.success("All patients stable ✅")
else:
    st.info("Initializing live simulation…")
