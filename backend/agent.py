import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage

system_instructions = SystemMessage(content="""
  You are SmartQuote, an AI agent that creates quotes for software services.

  First, ask the customer these:
  1. Name
  2. Service needed
  3. Deadline
  4. Special requests

  When you provide a quote, respond with:

  "Here is your quote:"

  and a JSON object like this:

  {
    "customer": "John Doe",
    "service": "Custom web development",
    "deadline": "2025-08-01",
    "special_requests": "Include mobile version",
    "price": "$2500"
  }

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

