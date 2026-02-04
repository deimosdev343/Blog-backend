from sqlalchemy import Column, UniqueConstraint, func, Text, ForeignKey
from sqlalchemy.orm import relationship 
from database import Base

class FollowModel(Base):
  __tablename__ = "following"
  
  Column("follower_id", ForeignKey("users.id"), primary_key=True),
  Column("followed_id", ForeignKey("users.id"), primary_key=True),
  UniqueConstraint("follower_id", "followed_id", name="uq_follows"),

  
