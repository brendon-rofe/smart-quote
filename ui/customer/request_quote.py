import streamlit as st
import requests

def response_generator(messages):
  data = {"messages": messages}
  response = requests.post(
    "http://127.0.0.1:8000/agent",
    json=data,
  )
  if response.status_code == 200:
    return response.json()
  else:
    return "Error: Failed to get response."

if "messages" not in st.session_state:
  st.session_state.messages = []
  st.session_state.messages.append({
      "role": "assistant",
      "content": "Hi! I'm SmartQuote 🤖. Let's create a software services quote! What's the customer's name?"
  })

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

if prompt := st.chat_input("How can I help you?"):
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  assistant_reply = response_generator(st.session_state.messages)

  with st.chat_message("assistant"):
    st.markdown(assistant_reply)
  st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
