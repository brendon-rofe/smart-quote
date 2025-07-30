from pydantic import BaseModel
from typing import Literal

class QuoteCreate(BaseModel):
  customer: str
  description: str
  price: int

#  TODO change role to enum
class UserCreate(BaseModel):
  username: str
  email: str
  password: str
  role: str

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

class CustomInstructionsCreate(BaseModel):
  custom_instructions: str | None
