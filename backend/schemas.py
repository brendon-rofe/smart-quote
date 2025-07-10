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
