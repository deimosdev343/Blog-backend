from sqlalchemy import Column, Integer, String, Float, Boolean,DateTime, func, Text, ForeignKey
from sqlalchemy.orm import relationship 
from database import Base

class FollowModel(Base):
  __tablename__ = "following"
  
  following_id = Column(Integer, primary_key=True, nullable=False)
  followee_id = Column(Integer, primary_key=True, nullable=False)
  

  
