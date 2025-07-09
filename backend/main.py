from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get_all_quotes():
  return {
    "Message": "This will return all quotes"
  }
