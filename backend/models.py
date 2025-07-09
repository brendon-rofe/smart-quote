from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Quote(Base):
  __tablename__ = "quotes"
  
  id = Column(Integer, primary_key=True, index=True)
  customer = Column(String, index=True)
  description = Column(String, index=True)
  price = Column(Integer, index=True)
