import streamlit as st
import requests
import time

if "role" not in st.session_state:
  st.session_state.role = None

if "customer_name" not in st.session_state:
  st.session_state.customer_name = None

ROLES = ["Customer", "Admin"]

def login():

  st.header("Log in")
  role = st.selectbox(
    "Choose your role:",
    ROLES,
    format_func=lambda r: "🛠️ Admin" if r == "Admin" else "👤 Customer"
  )

  with st.form("customer_login_form"):
    username = st.text_input("Enter your username:")
    password = st.text_input("Enter your password:")
    login = st.form_submit_button("Login")
    
    if login:
      if username == "" and password == "":
        st.warning("Please enter your username and password")
      elif username == "":
        st.warning("Please enter your username")
      elif password == "":
        st.warning("Please enter your password")
      else:
        response = requests.get(f"http://127.0.0.1:8000/users/{username}")
        user = response.json()
        if role != user["role"]:
          st.warning("Please select the correct role")
        elif password == user["password"]:
          st.session_state.customer_name = username
          st.success("Login successful!")
          time.sleep(1)
          st.session_state.role = role
          st.rerun()
        else:
          st.error("Incorrect username or password")

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
custom_instructions_page = st.Page("admin/custom_instructions.py", title="Set Custom Instructions", icon=":material/tune:")

register_page = st.Page("register.py", title="Register", icon=":material/person_add:")

account_pages = [logout_page, settings]
customer_pages = [customer_request_quote_page, customer_quotes_page]
admin_pages = [all_quotes_page, create_quote_page, custom_instructions_page]

page_dict = {}
if st.session_state.role == "Customer":
  page_dict["Quotes"] = customer_pages
if st.session_state.role == "Admin":
  page_dict["Quotes"] = admin_pages

if len(page_dict) > 0:
  pg = st.navigation({"Account": account_pages} | page_dict)
else:
  pg = st.navigation([register_page, st.Page(login)])

pg.run()
