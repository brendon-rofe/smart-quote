import streamlit as st

with st.form("custom_instructions_form"):
  custom_instructions = st.text_area("Enter your custom instructions here...")
  submit = st.form_submit_button("Submit")
  

if submit:
  st.success(custom_instructions)
