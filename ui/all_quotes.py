import streamlit as st
import requests
import time

st.header("All Quotes:")

if "editing_quote" not in st.session_state:
  st.session_state.editing_quote = None

with st.spinner():
  response = requests.get("http://127.0.0.1:8000/quotes")
  if response.status_code == 200:
    quotes = response.json()
    for i, quote in enumerate(quotes):
      st.divider()
      st.header(f"Customer: {quote['customer']}")
      st.write(f"Description: {quote['description']}")
      st.write(f"Price: {quote['price']}")

      col1, col2 = st.columns(2)

      with col1:
        if st.button("Edit Quote", key=f"button1_{i}"):
          st.session_state.editing_quote = i

      with col2:
        if st.button("Delete Quote", type="primary", key=f"button2_{i}"):
          with st.spinner("Deleting quote..."):
            response = requests.delete(f"http://127.0.0.1:8000/quotes/{quote['id']}")
          if response.status_code == 204:
            st.success("Quote deleted successfully!")
            time.sleep(3)
            st.rerun()
          else:
            st.error("Failed to delete quote")

      if st.session_state.editing_quote == i:
        with st.form(f"edit_quote_form_{i}"):
          customer = st.text_input("Enter customer", value=quote["customer"], key=f"customer_{i}")
          description = st.text_area("Enter description", value=quote["description"], key=f"description_{i}")
          price = st.number_input("Enter a price", value=quote["price"], key=f"price_{i}")

          col1, col2 = st.columns(2)
          submit = col1.form_submit_button("Apply Changes")
          cancel = col2.form_submit_button("Cancel")

          if submit:
            data = {
              "customer": customer,
              "description": description,
              "price": price,
            }
            with st.spinner("Updating quote..."):
              response = requests.put(
                f"http://127.0.0.1:8000/quotes/{quote['id']}",
                json=data
              )
            if response.status_code == 200:
              st.success("Quote updated successfully!")
              st.session_state.editing_quote = None
              time.sleep(3)
              st.rerun()
            else:
              st.error("Failed to update quote")
          
          if cancel:
            st.session_state.editing_quote = None
            st.rerun()
