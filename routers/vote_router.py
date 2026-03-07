from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from dto.user_dto import UserCreate, UserLogin, updateAvatar, updateUserDetails
from dto.folllow_dto import FollowUser
from models.user_model import UserModel, followers
from models.post_model import Post, PostVote
from database import SessionLocal
from utils.hash import hash_password, verify_password
from utils.auth import create_access_token
from utils.auth_scheme import get_current_user, blacklist_token
from sqlalchemy import update, insert, delete, select, func
from routers.userposts import userposts_router

router = APIRouter(
  prefix="/vote"
)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@router.post("/${post_id}")
def vote(
  post_id: int,
  vote: int,
  db: Session = Depends(get_db),
  user = Depends(get_current_user)
):
  post = db.query(Post).filter(Post.id == post_id).first()
  if not post:
    raise HTTPException(status_code=404, detail="Post not found")
  if vote not in [-1, 1]:
    raise HTTPException(400, "Vote must be -1, or 1")
  stmt = select(PostVote).where(
      PostVote.user_id == user["id"],
      PostVote.post_id == post_id
  )
  existing_vote = db.execute(stmt).scalar_one_or_none()
  if existing_vote:
    db.delete(existing_vote)
    if existing_vote.vote == vote:
      return {"msg":"vote successfully removed"}
  db.add(PostVote(
    user_id = user["id"],
    post_id = post_id,
    vote = vote
  ))
  db.commit()
  return {"msg":"vote updated"};
   
    
  