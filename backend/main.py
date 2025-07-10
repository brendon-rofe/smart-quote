from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_db, engine
from schemas import Quote, QuoteCreate, QuoteUpdate
from models import Base, QuoteModel

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
  