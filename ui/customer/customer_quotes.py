import streamlit as st
import requests
import time

if "deleting_quote" not in st.session_state:
  st.session_state.deleting_quote = None

st.title("All your quotes:")

def display_all_customer_quotes(customer_name):
  response = requests.get(f"http://127.0.0.1:8000/quotes/{customer_name}")
  if response.status_code == 404:
    st.warning("🤷‍♂️ You don't seem to be any quotes at the moment...")
  if response.status_code == 200:
    customer_quotes = response.json()
    for i, quote in enumerate(customer_quotes):
      st.divider()
      st.write(f"Description: {quote['description']}")
      st.write(f"Price: {quote['price']}")
      
      if st.button("Delete Quote", type="primary", key=f"{i}"):
        response = requests.delete(f"http://127.0.0.1:8000/quotes/{quote['id']}")
        st.session_state.deleting_quote = i
        if response.status_code == 204:
          st.success("Quote deleted successfully!")
          time.sleep(1)
          st.session_state.deleting_quote = None
          st.rerun()
      
display_all_customer_quotes(st.session_state.customer_name)
