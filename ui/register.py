import streamlit as st

st.title("Register")

with st.form("registration_form"):
  st.text_input("username")
  st.text_input("email")
  st.text_input("password")
  st.text_input("role")
  st.form_submit_button("Register")
