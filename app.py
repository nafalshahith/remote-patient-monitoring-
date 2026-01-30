import streamlit as st
import pandas as pd
from datagen import stream_data
from riskmode import predict_risk
import streamlit.components.v1 as components

# ---- FORCE PAGE REFRESH EVERY 2 SECONDS ----
components.html(
    """
    <script>
        setTimeout(function(){
            window.location.reload();
        }, 2000);
    </script>
    """,
    height=0,
)

st.set_page_config(page_title="Remote Patient Monitoring", layout="wide")

st.title("🏥 Remote Patient Monitoring Dashboard")
st.markdown("Live simulated patient vitals (updates every 2 seconds)")

# ---- SESSION STATE ----
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame()

# ---- CONTROLS ----
num_patients = st.sidebar.slider("Number of Patients", 1, 10, 5)

# ---- GENERATE NEW DATA ON EVERY RELOAD ----
new_data = stream_data(num_patients)
new_data["Risk Level"] = new_data.apply(predict_risk, axis=1)

st.session_state.data = pd.concat(
    [st.session_state.data, new_data],
    ignore_index=True
).tail(300)

# ---- CURRENT SNAPSHOT ----
st.subheader("📊 Current Vitals")
st.dataframe(new_data, use_container_width=True)

# ---- LIVE CHARTS ----
col1, col2 = st.columns(2)

with col1:
    st.subheader("❤️ Heart Rate (Live)")
    hr_df = st.session_state.data.pivot(
        index="timestamp",
        columns="patient_id",
        values="heart_rate"
    )
    st.line_chart(hr_df)

with col2:
    st.subheader("🫁 SpO₂ (Live)")
    spo2_df = st.session_state.data.pivot(
        index="timestamp",
        columns="patient_id",
        values="spo2"
    )
    st.line_chart(spo2_df)

# ---- ALERTS ----
st.subheader("🚨 Live Alerts")
alerts = st.session_state.data[
    st.session_state.data["Risk Level"] == "High Risk"
]

if not alerts.empty:
    st.error("⚠ High Ri
