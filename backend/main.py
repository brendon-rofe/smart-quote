from fastapi import FastAPI
from contextlib import asynccontextmanager
from pydantic import BaseModel

from database import get_db, engine
from models import Base, Quote

class Quote(BaseModel):
  id: int
  customer: str
  description: str
  price: int

@asynccontextmanager
async def lifespan(app: FastAPI):
  async with engine.begin() as connection:
    await connection.run_sync(Base.metadata.create_all)
  yield

app = FastAPI(lifespan=lifespan)

@app.get("/quotes")
def get_all_quotes():
  return {
    "Message": "This will return all quotes"
  }
