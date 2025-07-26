import streamlit as st
import requests

st.title("All your quotes:")

def display_all_customer_quotes(customer_name):
  response = requests.get(f"http://127.0.0.1:8000/quotes/{customer_name}")
  if response.status_code == 404:
    st.warning("🤷‍♂️ You don't seem to be any quotes at the moment...")
  if response.status_code == 200:
    customer_quotes = response.json()
    for quote in customer_quotes:
      st.divider()
      st.write(f"Description: {quote['description']}")
      st.write(f"Price: {quote['price']}")
      
display_all_customer_quotes(st.session_state.customer_name)
