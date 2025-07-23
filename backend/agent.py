import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
import httpx

load_dotenv()

llm = ChatGoogleGenerativeAI(
  model="gemini-2.0-flash",
  google_api_key=os.getenv("GOOGLE_API_KEY")
)

async def get_custom_data():
  async with httpx.AsyncClient() as client:
    response = await client.get("http://127.0.0.1:8000/custom-data")
    response.raise_for_status()
    return response

async def prompt_llm(messages):
  custom_data = await get_custom_data()
  data = custom_data.json()
  print("custom data:", data)

  system_instructions = SystemMessage(content=f"""
    You are SmartQuote, an AI agent that creates quotes using the below custom instructions and PDF text.

    CUSTOM INSTRUCTIONS:
    {data['custom_instructions']}

    PDF TEXT:
    {data['pdf_text']}

    First, ask the customer these one at a time:
    1. Name
    2. Service needed
    3. Special requests

    When you provide a quote, respond with a JSON object like this:

    {{
      "customer": "John Doe",
      "description": "Custom web development",
      "price": "2500"
    }}

    Place the services needed and any special requests into the description.

    If you are still collecting info, just reply with your next question.
  """)

  full_messages = [system_instructions] + messages
  response = await llm.ainvoke(full_messages)
  return response.content
