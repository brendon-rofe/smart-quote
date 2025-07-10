from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_db, engine
from schemas import Quote, QuoteCreate
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
