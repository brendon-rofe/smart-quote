import streamlit as st
import requests
import re
import json

def extract_json(text):
  match = re.search(r'\{.*\}', text, re.DOTALL)
  if match:
    json_str = match.group()
    try:
      return json.loads(json_str)
    except json.JSONDecodeError:
      return None
  return None

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

def send_quote_to_backend(quote_data):
  payload = {
    "customer": quote_data.get("customer"),
    "description": quote_data.get("description"),
    "price": quote_data.get("price").replace("$", "").strip()  # clean up $ sign
  }
  response = requests.post(
    "http://127.0.0.1:8000/quotes",
    json=payload,
  )
  if response.status_code == 200:
    st.success("✅ Your quote has been saved!")
  else:
    st.error(f"❌ Failed to save quote: {response.text}")


if "messages" not in st.session_state:
  st.session_state.messages = []
  st.session_state.messages.append({
      "role": "assistant",
      "content": "Hi! I'm SmartQuote 🤖. Let's create a software services quote! What's the customer's name?"
  })

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    if message["role"] == "assistant":
      json_data = extract_json(message["content"])
      if json_data:
        print(json_data)
        st.markdown("**Here is your quote:**")
        st.write(f"Customer: {json_data.get('customer', '')}")
        st.write(f"Description: {json_data.get('description', '')}")
        st.write(f"Price: {json_data.get('price', '')}")
        
        if all(k in json_data for k in ["customer", "description", "price"]):
          send_quote_to_backend(json_data)
      else:
        st.markdown(message["content"])
    else:
      st.markdown(message["content"])

if prompt := st.chat_input("How can I help you?"):
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  assistant_reply = response_generator(st.session_state.messages)

  with st.chat_message("assistant"):
    json_data = extract_json(assistant_reply)

    if json_data:
      st.markdown("**Here is your quote:**")
      st.write(f"Customer: {json_data.get('customer', '')}")
      st.write(f"Description: {json_data.get('description', '')}")
      st.write(f"Price: {json_data.get('price', '')}")

    else:
      st.markdown(assistant_reply)

  st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
