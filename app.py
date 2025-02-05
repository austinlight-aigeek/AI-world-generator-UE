import streamlit as st
import requests

API_URL = "http://localhost:8000/generate"  # Update if deployed

st.title("AI World Generator 🌍🚀")
prompt = st.text_input("Enter your world prompt", "Generate a futuristic city")

if st.button("Generate World"):
    response = requests.post(API_URL, json={"prompt": prompt})
    if response.status_code == 200:
        st.json(response.json())  # Display JSON Output
    else:
        st.error("Failed to generate world, check API logs.")
