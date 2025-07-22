import streamlit as st
import requests

with st.form("custom_instructions_form"):
  custom_instructions = st.text_area("Enter your custom instructions here...")
  submit = st.form_submit_button("Submit")
  

if submit:
  data = {
      "custom_instructions": custom_instructions,
    }
  with st.spinner("Creating quote..."):
    response = requests.post(
      "http://127.0.0.1:8000/custom-instructions",
      json = data
    )
  if response.status_code == 200:
    st.success("✅ Your custom instructions have been saved!")
  else:
    st.error(f"❌ Failed to save custom instructions: {response.text}")
