import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage

system_instructions = SystemMessage(content="""
  You are SmartQuote, an AI agent that creates quotes for software services.

  First, ask the customer these:
  1. Name
  2. Service needed
  4. Special requests

  When you provide a quote, respond with a JSON object like this:

  {
    "customer": "John Doe",
    "description": "Custom web development",
    "price": "2500"
  }

  Place the services needed and any special requests into the description

  If you are still collecting info, just reply with your next question
""")

load_dotenv()

llm = ChatGoogleGenerativeAI(
  model="gemini-2.0-flash",
  google_api_key=os.getenv("GOOGLE_API_KEY")
)

async def prompt_llm(messages):
  full_messages = [system_instructions] + messages
  response = await llm.ainvoke(full_messages)
  return response.content
