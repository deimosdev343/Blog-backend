from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class UserModel(Base):
  __tablename__ = "users"
  
  id = Column(Integer, primary_key=True, nullable=False)
  username = Column(String(100), unique=True, nullable=False)
  hashed_password = Column(String(100), nullable=False)
  
  