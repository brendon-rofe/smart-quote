import streamlit as st
import requests

st.header("All Quotes:")

with st.spinner():
  response = requests.get("http://127.0.0.1:8000/quotes")
  if response.status_code == 200:
    quotes = response.json()
    for i, quote in enumerate(quotes):
      st.divider()
      st.header(f"Customer: {quote["customer"]}")
      st.write(f"Description: {quote["description"]}")
      st.write(f"Price: {quote["price"]}")
      col1, col2, _ = st.columns([1, 1, 3])
      
      with col1:
        st.button("Edit Quote", key=f"button1_{i}")

      with col2:
          st.button("Delete Quote", type="primary", key=f"button2_{i}")
