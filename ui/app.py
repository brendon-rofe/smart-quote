import streamlit as st
import requests
import json

st.title("SmartQuote")

with st.spinner():
  response = requests.get("http://127.0.0.1:8000/quotes")
  if response.status_code == 200:
    quotes = response.json()
    for quote in quotes:
      st.divider()
      st.header(f"Customer: {quote["customer"]}")
      st.write(f"Description: {quote["description"]}")
      st.write(f"Price: {quote["price"]}")  
