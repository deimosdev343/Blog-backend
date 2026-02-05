from sqlalchemy import Column, Integer, String, DateTime, Table,ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import relationship
from database import Base


#блять как же я тут навасанила

followers = Table(
  'followers',
  Base.metadata,
  Column('follower_id', Integer, ForeignKey('users.id'), primary_key=True),
  Column('followed_id', Integer, ForeignKey('users.id'), primary_key=True),
  UniqueConstraint("follower_id", "followed_id", name="uq_follows")
)

class UserModel(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, nullable=False)
  username = Column(String(100), unique=True, nullable=False)
  hashed_password = Column(String(100), nullable=False)
  email = Column(String(100), unique=True, nullable=False)
  created_at = Column(DateTime, default=func.now())
  avatar_url = Column(String(500), nullable = True)
  
  following = relationship(
    "UserModel",
    secondary=followers,
    primaryjoin=(followers.c.follower_id == id),
    secondaryjoin=(followers.c.followed_id == id),
    back_populates='follwers'
  )
  
  
