from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class QuoteModel(Base):
  __tablename__ = "quotes"
  
  id = Column(Integer, primary_key=True, index=True)
  customer = Column(String(255), index=True)
  description = Column(String(255), index=True)
  price = Column(Integer, index=True)
