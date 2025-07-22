from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy import Enum

import enum

class UserRoleEnum(enum.Enum):
  Admin = "Admin"
  Customer = "Customer"

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
  role = Column(Enum(UserRoleEnum), nullable=False)

class CustomInstructionsModel(Base):
  __tablename__ = "custom_instructions"
  
  id = Column(Integer, primary_key=True, index=True)
  custom_instructions = Column(String(255))
