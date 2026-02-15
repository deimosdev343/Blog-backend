from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.post_model import Post 
from models.user_model import UserModel

from database import SessionLocal
from dto.post_dto import PostCreate
from utils.auth_scheme import get_current_user

router = APIRouter(
  prefix="/posts"
)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@router.get('/{user_id}')
def get_posts_for_user(
    user_id: int,
    skip:int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)):
    return (
        db.query(Post)
            .filter(Post.author_id == user_id )
            .order_by(Post.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
    ) 