import streamlit as st

st.title("Import Test")

try:
    import datagen
    st.success("datagen.py imported successfully")
except Exception as e:
    st.error(f"datagen error: {e}")

try:
    import riskmode
    st.success("riskmode.py imported successfully")
except Exception as e:
    st.error(f"riskmode error: {e}")
