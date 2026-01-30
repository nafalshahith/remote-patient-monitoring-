import streamlit as st
import time
import pandas as pd
from datagen import stream_data
from riskmode import predict_risk

st.set_page_config(page_title="Remote Patient Monitoring", layout="wide")

st.title("🏥 Remote Patient Monitoring Dashboard")
st.markdown("Live monitoring of patient vitals with AI risk prediction")

# Session state to store streaming data
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame()

# Sidebar controls
st.sidebar.header("Controls")
num_patients = st.sidebar.slider("Number of Patients", 1, 10, 5)
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 1, 5, 2)

placeholder = st.empty()

while True:
    new_data = stream_data(num_patients)
    new_data["Risk Level"] = new_data.apply(predict_risk, axis=1)

    st.session_state.data = pd.concat(
        [st.session_state.data, new_data]
    ).tail(200)

    with placeholder.container():
        st.subheader("📊 Live Patient Vitals")
        st.dataframe(new_data, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("❤️ Heart Rate")
            st.line_chart(
                st.session_state.data.pivot(
                    index="timestamp",
                    columns="patient_id",
                    values="heart_rate"
                )
            )

        with col2:
            st.subheader("🫁 SpO2 Levels")
            st.line_chart(
                st.session_state.data.pivot(
                    index="timestamp",
                    columns="patient_id",
                    values="spo2"
                )
            )

        st.subheader("🚨 Alerts")
        alerts = new_data[new_data["Risk Level"] == "High Risk"]

        if not alerts.empty:
            st.error("⚠ CRITICAL PATIENT ALERTS!")
            st.dataframe(alerts, use_container_width=True)
        else:
            st.success("All patients stable ✅")

    time.sleep(refresh_rate)
