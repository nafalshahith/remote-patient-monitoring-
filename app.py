import streamlit as st
import pandas as pd
from streamlit_extras.st_autorefresh import st_autorefresh
from datagen import stream_data
from riskmode import predict_risk

st.set_page_config(page_title="Remote Patient Monitoring", layout="wide")

st.title("🏥 Remote Patient Monitoring Dashboard")
st.markdown("Live simulated patient vitals (updates every 2 seconds)")

# ---- AUTO REFRESH (STABLE) ----
st_autorefresh(interval=2000, key="live")

# ---- SESSION STATE ----
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame()

# ---- CONTROLS ----
num_patients = st.sidebar.slider("Number of Patients", 1, 10, 5)

# ---- GENERATE DATA EVERY REFRESH ----
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
    st.line_chart(
        st.session_state.data.pivot(
            index="timestamp",
            columns="patient_id",
            values="heart_rate"
        )
    )

with col2:
    st.subheader("🫁 SpO₂ (Live)")
    st.line_chart(
        st.session_state.data.pivot(
            index="timestamp",
