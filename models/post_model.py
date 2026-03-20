from sqlalchemy import Column, Integer, String, Float, Boolean,DateTime, func, Text, ForeignKey, UniqueConstraint 
from sqlalchemy.orm import relationship 
from database import Base


class Post(Base):
  __tablename__= "posts"
  
  id = Column(Integer, primary_key=True)
  author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  title = Column(String(100), nullable=False)
  content = Column(Text(300000), nullable=False)
  username = Column(String(100), nullable= False)
  user_avatar = Column(String(500), nullable=True)
  created_at = Column(DateTime, default=func.now())
  updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
  
class PostVote(Base):
  __tablename__ = "post_votes"
  user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
  post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
  vote = Column(Integer)
  
  __table_args__ = (
    UniqueConstraint("user_id", "post_id", name="uq_user_post_vote"),
  )
  
class PostComment(Base):
  __tablename__ = "post_comments"
  
  id = Column(Integer, primary_key=True)
  post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
  author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  title = Column(String(100), nullable=False)
  content = Column(Text(300000), nullable=False)
  username = Column(String(100), nullable= False)
  user_avatar = Column(String(500), nullable=True)
  created_at = Column(DateTime, default=func.now())
  updated_at = Column(DateTime, default=func.now(), onupdate=func.now())