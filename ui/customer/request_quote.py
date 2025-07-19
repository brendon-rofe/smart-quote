import streamlit as st
import requests

def response_generator(prompt):
  with st.spinner("Thinking..."):
    data = {"prompt": prompt}
    response = requests.post(
      "http://127.0.0.1:8000/agent",
      json = data,
    )
    if response.status_code == 200:
      return response.json()

if "messages" not in st.session_state:
  st.session_state.messages = []

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  with st.chat_message("assistant"):
    response = st.write(response_generator(prompt))
  st.session_state.messages.append({"role": "assistant", "content": response})
