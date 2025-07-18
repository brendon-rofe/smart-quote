import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatGoogleGenerativeAI(
  model="gemini-2.0-flash",
  google_api_key=os.getenv("GOOGLE_API_KEY"),
  streaming=True
)

async def prompt_llm(prompt: str):
  async for chunk in llm.astream([HumanMessage(content=prompt)]):
    yield f"data: {chunk.content}\n\n"
