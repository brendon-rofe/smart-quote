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
      
      if st.button("Edit Quote", key=f"button1_{i}"):
        with st.form("edit_quote_form"):
          customer = st.text_input("Enter customer", value=f"{quote["customer"]}")
          description =  st.text_area("Enter description", value=f"{quote["description"]}")
          price = st.number_input("Enter a price", value=quote["price"])
          submit = st.form_submit_button("Apply Changes")

      st.button("Delete Quote", type="primary", key=f"button2_{i}")
