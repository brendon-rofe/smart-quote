from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Quote(BaseModel):
  id: int
  customer: str
  description: str
  price: int

@app.get("/")
def get_all_quotes():
  return {
    "Message": "This will return all quotes"
  }
