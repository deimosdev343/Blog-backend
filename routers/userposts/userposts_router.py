from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, func, case
from models.post_model import Post, PostVote 
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
    stmt = (
        select(
            Post,
            func.sum(
                case((PostVote.vote == 1, 1), else_=0),
            ).label("upvotes"),
            func.sum(
                case((PostVote.vote == -1, 1), else_=0),
            ).label("downvotes"),
        )
        .outerjoin(PostVote, PostVote.post_id == Post.id)
        .where(Post.author_id == user_id)
        .group_by(Post.id)
        .order_by(Post.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    results = db.execute(stmt).all()
    
    posts = []
    
    for post, upvotes, downvotes in results:
      posts.append({
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author_id": post.author_id,
        "username": post.username,
        "user_avatar": post.user_avatar,
        "created_at": post.created_at,
        "upvotes": upvotes,
        "downvotes": downvotes
      })
    return posts