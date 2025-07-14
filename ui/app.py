import streamlit as st

st.title("SmartQuote")

pg = st.navigation([st.Page("create_quote.py"), st.Page("all_quotes.py")])

pg.run()
