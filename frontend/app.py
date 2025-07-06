import streamlit as st
import requests

# Replace with your deployed FastAPI backend URL
FASTAPI_URL = "https://calendar-chatbot-w2dr.onrender.com" or "http://localhost:8000/chat"

st.set_page_config(page_title="Calendar Assistant", page_icon="📅")
st.title("AI Calendar Assistant")

st.markdown("Ask me to book meetings, check availability, and more!")

# User input
user_input = st.text_input("What would you like to do?", placeholder="e.g., Book a meeting titled Standup on 2025-07-08 at 10:00")

if st.button("Send") or user_input:
    if user_input.strip() == "":
        st.warning("Please enter a message.")
    else:
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    FASTAPI_URL,
                    json={"message": user_input},
                    timeout=30
                )
                if response.status_code == 200:
                    result = response.json()
                    st.success(result.get("response", "No response"))
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")
