import streamlit as st
import requests

with st.form("custom_instructions_form"):
  custom_instructions = st.text_area("Enter your custom instructions here...")
  submit = st.form_submit_button("Submit")
  

if submit:
  data = {
      "custom_instructions": custom_instructions,
    }
  with st.spinner("Creating custom instructions..."):
    response = requests.post(
      "http://127.0.0.1:8000//custom-data/instructions",
      json = data
    )
  if response.status_code == 200:
    st.success("✅ Your custom instructions have been saved!")
  else:
    st.error(f"❌ Failed to save custom instructions: {response.text}")

uploaded_file = st.file_uploader(
    "Upload a PDF file", accept_multiple_files=False
)

if uploaded_file is not None:
  bytes_data = uploaded_file.read()
  st.write("filename:", uploaded_file.name)

  files = {
      "pdf_file": (uploaded_file.name, bytes_data, uploaded_file.type)
  }

  response = requests.post("http://127.0.0.1:8000/custom-data/upload-pdf", files=files)

  if response.status_code == 200:
      st.success(f"{uploaded_file.name} uploaded successfully!")
  else:
      st.error(f"Failed to upload {uploaded_file.name}: {response.text}")

