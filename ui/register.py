import streamlit as st
import requests

st.title("Register")

with st.form("registration_form"):
  user_username = st.text_input("username")
  user_email = st.text_input("email")
  user_password = st.text_input("password")
  user_role = st.text_input("role")
  submit = st.form_submit_button("Register")
  
  if submit:
    data = {
      "username": user_username,
      "email": user_email,
      "password": user_password,
      "role": user_role
    }
    response = requests.post(
      "http://127.0.0.1:8000/users",
      json = data
    )
    if response.status_code == 200:
      st.success("You have successfully been registered!")
    else:
      st.error("Failed to register")
