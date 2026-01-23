from sqlalchemy import Column, Integer, String, Float, Boolean,DateTime, func, Text, ForeignKey
from sqlalchemy.orm import relationship 
from database import Base
from datetime import datetime, timezone

class Post(Base):
  __tablename__= "posts"
  
  id = Column(Integer, primary_key=True)
  author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  title = Column(String(100), nullable=False)
  content = Column(Text(100000), nullable=False)
  created_at = Column(DateTime, default=timezone.utc)
  updated_at = Column(DateTime, default=timezone.utc, onupdate=timezone.utc)
  