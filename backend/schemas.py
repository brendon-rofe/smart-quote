from pydantic import BaseModel

class QuoteCreate(BaseModel):
  customer: str
  description: str
  price: int

class Quote(BaseModel):
  id: int
  customer: str
  description: str
  price: int

  class Config:
    orm_mode = True

class QuoteUpdate(BaseModel):
  customer: str | None = None
  description: str | None = None
  price: int | None = None
