from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_db, engine
from models import Base, QuoteModel

class Quote(BaseModel):
    id: int
    customer: str
    description: str
    price: int

    class Config:
        orm_mode = True

@asynccontextmanager
async def lifespan(app: FastAPI):
  async with engine.begin() as connection:
    await connection.run_sync(Base.metadata.create_all)
  yield

app = FastAPI(lifespan=lifespan)

@app.get("/quotes", response_model=List[Quote])
async def get_all_quotes(db: AsyncSession = Depends(get_db)):
  result = await db.execute(select(QuoteModel))
  quotes = result.scalars().all()
  return quotes
