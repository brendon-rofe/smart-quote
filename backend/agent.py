import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage

system_instructions = SystemMessage(content="""
  You are SmartQuote, an AI agent that creates quotes for software services.
  First, ask the customer:
  1. Name
  2. Service needed
  3. Deadline
  4. Special requests

  At the end, summarize the quote like:
  ---
  Customer: NAME
  Service: DESCRIPTION
  Deadline: DATE
  Price: $ AMOUNT
""")

load_dotenv()

llm = ChatGoogleGenerativeAI(
  model="gemini-2.0-flash",
  google_api_key=os.getenv("GOOGLE_API_KEY")
)

async def prompt_llm(prompt: str):
  messages = [system_instructions, HumanMessage(content=prompt)]
  response = await llm.ainvoke(messages)
  return response.content
