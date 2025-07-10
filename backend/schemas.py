from pydantic import BaseModel

class Quote(BaseModel):
    id: int
    customer: str
    description: str
    price: int

    class Config:
        orm_mode = True
