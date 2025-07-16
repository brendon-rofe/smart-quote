import streamlit as st

if "role" not in st.session_state:
  st.session_state.role = None

ROLES = ["Customer", "Admin"]

def login():

  st.header("Log in")
  role = st.selectbox(
    "Choose your role",
    ROLES,
    format_func=lambda r: "🛠️ Admin" if r == "Admin" else "👤 Customer"
  )

  if st.button("Log in"):
    st.session_state.role = role
    st.rerun()

def logout():
  st.session_state.role = None
  st.rerun()

role = st.session_state.role

logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
settings = st.Page("settings.py", title="Settings", icon=":material/settings:")
customer_request_quote_page = st.Page(
  "customer/request_quote.py",
  title="Request a Quote",
  icon=":material/help:",
  default=(role == "Customer"),
)
customer_quotes_page = st.Page(
  "customer/customer_quotes.py", title="Your Quotes", icon=":material/assignment:"
)
all_quotes_page = st.Page(
  "admin/all_quotes.py",
  title="All Quotes",
  default=(role == "Admin"), icon=":material/list:"
)
create_quote_page = st.Page("admin/create_quote.py", title="Create Quote", icon=":material/edit:")

account_pages = [logout_page, settings]
customer_pages = [customer_request_quote_page, customer_quotes_page]
admin_pages = [all_quotes_page, create_quote_page]

st.title("Request manager")

page_dict = {}
if st.session_state.role == "Customer":
  page_dict["Quotes"] = customer_pages
if st.session_state.role == "Admin":
  page_dict["Quotes"] = admin_pages

if len(page_dict) > 0:
  pg = st.navigation({"Account": account_pages} | page_dict)
else:
  pg = st.navigation([st.Page(login)])

pg.run()