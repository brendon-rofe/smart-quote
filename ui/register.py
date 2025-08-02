import streamlit as st

st.title("Register")

with st.form("registration_form"):
  user_username = st.text_input("username")
  user_email = st.text_input("email")
  user_password = st.text_input("password")
  user_role = st.text_input("role")
  st.form_submit_button("Register")
