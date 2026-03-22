from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from models.post_model import PostComment
from database import SessionLocal
from utils.auth_scheme import get_current_user, blacklist_token, get_current_user_if_logged_in
from sqlalchemy import update, insert, delete, select, func, case

router = APIRouter(
  prefix="/comment"
);

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@router.get("/{post_id}")
def get_post_comments(
  post_id: int,
  db: Session = Depends(get_db),
  current_user = Depends(get_current_user)
):
  comments = db.query(PostComment).filter(PostComment.post_id == post_id).first()
  return comments;
  
  