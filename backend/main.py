from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from contextlib import asynccontextmanager
from typing import List
from langchain_core.messages import HumanMessage, AIMessage
import base64
import io
from PyPDF2 import PdfReader

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_db, engine
from schemas import (
    Quote,
    QuoteCreate,
    QuoteUpdate,
    CustomInstructionsCreate,
  )
from models import Base, QuoteModel, UserModel, CustomDataModel

from pydantic import BaseModel
from agent import prompt_llm

class Message(BaseModel):
  role: str
  content: str

class Conversation(BaseModel):
  messages: list[Message]

def extract_text_from_base64_pdf(base64_string: str) -> str:
  try:
    pdf_bytes = base64.b64decode(base64_string)

    reader = PdfReader(io.BytesIO(pdf_bytes))
    extracted_text = ""
    for page in reader.pages:
      page_text = page.extract_text()
      if page_text:
        extracted_text += page_text + "\n"

    return extracted_text.strip()

  except Exception as e:
    print(f"Error extracting PDF text: {e}")
    return ""

@asynccontextmanager
async def lifespan(app: FastAPI):
  async with engine.begin() as connection:
    await connection.run_sync(Base.metadata.create_all)
  yield

app = FastAPI(lifespan=lifespan)

@app.post("/quotes", response_model=Quote)
async def create_quote(quote: QuoteCreate, db: AsyncSession = Depends(get_db)):
  new_quote = QuoteModel(
    customer = quote.customer,
    description = quote.description,
    price = quote.price
  )
  db.add(new_quote)
  await db.commit()
  await db.refresh(new_quote)
  return new_quote

@app.get("/quotes", response_model=List[Quote])
async def get_all_quotes(db: AsyncSession = Depends(get_db)):
  result = await db.execute(select(QuoteModel))
  quotes = result.scalars().all()
  if not quotes:
    raise HTTPException(status_code=404, detail="No quotes found")
  return quotes

@app.put("/quotes/{quote_id}")
async def update_quote(quote_id: int, quote: QuoteUpdate, db: AsyncSession = Depends(get_db)):
  result = await db.execute(select(QuoteModel).where(QuoteModel.id == quote_id))
  existing_quote = result.scalars().first()
  
  if not existing_quote:
    raise HTTPException(status_code=404, detail="Quote not found")
  
  if quote.customer is not None:
    existing_quote.customer = quote.customer
  if quote.description is not None:
    existing_quote.description = quote.description
  if quote.price is not None:
    existing_quote.price = quote.price
    
  await db.commit()
  await db.refresh(existing_quote)
  return existing_quote
  
@app.delete("/quotes/{quote_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_quote(quote_id: int, db: AsyncSession = Depends(get_db)):
  result = await db.execute(select(QuoteModel).where(QuoteModel.id == quote_id))
  quote = result.scalars().first()
  
  if not quote:
    raise HTTPException(status_code=404, detail="Quote not found")

  await db.delete(quote)
  await db.commit()
  return {"detail": "Quote deleted successfully"}

@app.get("/users/{username}")
async def get_user_by_username(username: str, db: AsyncSession = Depends(get_db)):
  result = await db.execute(select(UserModel).where(UserModel.username == username))
  user = result.scalars().first()
  if not user:
    raise HTTPException(status_code=404, detail="User with that username not found")
  return user

@app.post("/agent")
async def prompt_agent(conversation: Conversation):
  chat_history = []
  for msg in conversation.messages:
    if msg.role == "user":
      chat_history.append(HumanMessage(content=msg.content))
    else:
      chat_history.append(AIMessage(content=msg.content))

  response = await prompt_llm(chat_history)
  return response

@app.post("/custom-data/instructions")
async def add_custom_instructions(custom_data: CustomInstructionsCreate, db: AsyncSession = Depends(get_db)):
  new_custom_instructions = CustomDataModel(
    custom_instructions = custom_data.custom_instructions,
  )
  db.add(new_custom_instructions)
  await db.commit()
  await db.refresh(new_custom_instructions)
  return new_custom_instructions

@app.post("/custom-data/upload-pdf")
async def upload_pdf(pdf_file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
  result = await db.execute(select(CustomDataModel))
  entry = result.scalar_one_or_none()
  if not entry:
      raise HTTPException(status_code=404, detail="Custom data entry not found")

  pdf_content = await pdf_file.read()
  entry.pdf_file = pdf_content

  await db.commit()
  await db.refresh(entry)

  return {"message": "PDF uploaded successfully"}

@app.get("/custom-data")
async def get_custom_data(db: AsyncSession = Depends(get_db)):
  result = await db.execute(select(CustomDataModel))
  entry = result.scalar_one_or_none()
  if not entry:
    raise HTTPException(status_code=404, detail="Custom data not found")
  pdf_base64 = base64.b64encode(entry.pdf_file).decode('utf-8') if entry.pdf_file else None

  pdf_text = extract_text_from_base64_pdf(pdf_base64)

  return {
    "id": entry.id,
    "custom_instructions": entry.custom_instructions,
    "pdf_text": pdf_text
  }
