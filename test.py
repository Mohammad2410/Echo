import requests
import streamlit as st

api_url = "http://127.0.0.1:8000/api/add_post/"  # Ensure this URL is correct

data = {"title": "Test Post", "content": "This is a test content"}
res = requests.post(api_url, json=data)

# 🔹 Print response status and text for debugging
print(f"Status Code: {res.status_code}")
print(f"Response Text: {res.text}")

# Try to parse JSON safely
try:
    json_data = res.json()
    st.success(json_data.get("message", "Success!"))
except requests.exceptions.JSONDecodeError:
    st.error("Invalid JSON response from server.")
