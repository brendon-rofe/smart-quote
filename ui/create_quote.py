import streamlit as st

st.header("Create A Quote:")

with st.form("create_quote_form"):
  st.text_input("Enter customer")
  st.text_area("Enter description")
  st.number_input("Enter a price")
  st.form_submit_button("Create Quote")
