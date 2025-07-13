import streamlit as st
import requests

st.header("Create A Quote:")

with st.form("create_quote_form"):
  customer = st.text_input("Enter customer")
  description =  st.text_area("Enter description")
  price = st.number_input("Enter a price")
  submit = st.form_submit_button("Create Quote")
  
  if submit:
    data = {
      "customer": customer,
      "description": description,
      "price": price,
    }
    response = requests.post(
      "http://127.0.0.1:8000/quotes",
      json = data
    )
    if response.status_code == 200:
      st.success("Quote created!")
    
