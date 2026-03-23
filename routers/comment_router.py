from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from models.post_model import PostComment, Post
from models.user_model import UserModel
from database import SessionLocal
from utils.auth_scheme import get_current_user, blacklist_token, get_current_user_if_logged_in
from sqlalchemy import update, insert, delete, select, func, case
from dto.comment_dto import CommentDto
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
  db: Session = Depends(get_db)
):
  comments = db.query(PostComment).filter(PostComment.post_id == post_id).first()
  return comments;

@router.post("/")
def create_post_comment(
  comment: CommentDto,
  db: Session = Depends(get_db),
  current_user = Depends(get_current_user)
):
  post = db.query(Post).filter(Post.id == comment.post_id).first()
  if not post:
    raise HTTPException(status_code=404, detail="Post not found")
  user_data = db.query(UserModel).filter(UserModel.username == current_user["username"]).first()

  db.add(PostComment(
    author_id = current_user["id"],
    content = comment.content,
    post_id = comment.post_id,
    username = current_user["username"],
    user_avatar = user_data.avatar_url
  ));
  db.commit()
  return {"msg":"commment created successfully"}
  