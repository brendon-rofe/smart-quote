import streamlit as st
import requests

def response_generator(prompt):
  data = {"prompt": prompt}
  with requests.post(
    "http://127.0.0.1:8000/agent",
    json=data,
    stream=True
  ) as response:
      for line in response.iter_lines():
        if line:
          decoded = line.decode("utf-8")
          if decoded.startswith("data: "):
            yield decoded.removeprefix("data: ").strip()

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
    response = st.write_stream(response_generator(prompt))
  st.session_state.messages.append({"role": "assistant", "content": response})
