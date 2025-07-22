from pydantic import BaseModel
from typing import Literal

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
    from_attributes  = True

class QuoteUpdate(BaseModel):
  customer: str | None = None
  description: str | None = None
  price: int | None = None

class User(BaseModel):
  id: int
  username: str
  email: str
  password: str
  role: Literal["Admin", "Customer"]

  class Config:
    from_attributes  = True

class CustomInstructions(BaseModel):
  id: int | None
  custom_instructions: str
  
  class Config:
    from_attributes  = True
