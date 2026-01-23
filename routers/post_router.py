from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.post_model import Post 
from database import SessionLocal
from dto.post_dto import PostCreate
from utils.auth_scheme import get_current_user
router = APIRouter(
  prefix="/posts",
  tags=["posts"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_post(post: PostCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    
    db_post = Post(
        author_id= user["id"],
        title=post.title,
        content=post.content
    )
    db.add(db_post)
    db.commit()
    return {"msg":"post created successfully"}

@router.get("/")
def get_posts(
    skip:int = 0, 
    limit: int = 10,
    db: Session = Depends(get_db)):
    return (
        db.query(Post)
            .order_by(Post.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
    )
    