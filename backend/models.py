from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class QuoteModel(Base):
  __tablename__ = "quotes"
  
  id = Column(Integer, primary_key=True, index=True)
  customer = Column(String(255))
  description = Column(String(255))
  price = Column(Integer)

class UserModel(Base):
  __tablename__ = "users"
  
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String(255))
  email = Column(String(255))
  password = Column(String(255))
