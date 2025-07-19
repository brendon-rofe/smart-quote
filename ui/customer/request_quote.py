import streamlit as st
import requests

def response_generator(prompt):
  with st.spinner("Thinking..."):
    data = {"prompt": prompt}
    response = requests.post(
      "http://127.0.0.1:8000/agent",
      json=data,
    )
    if response.status_code == 200:
      return response.json()["response"]
    else:
      return "Error: Failed to get response."

# Initialize chat history
if "messages" not in st.session_state:
  st.session_state.messages = []

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  assistant_reply = response_generator(prompt)

  with st.chat_message("assistant"):
    st.markdown(assistant_reply)
  st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
