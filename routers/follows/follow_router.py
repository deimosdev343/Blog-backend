from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from dto.user_dto import UserCreate, UserLogin, updateAvatar, updateUserDetails
from models.user_model import UserModel, followers
from models.post_model import Post
from database import SessionLocal
from utils.hash import hash_password, verify_password
from utils.auth import create_access_token
from utils.auth_scheme import get_current_user, blacklist_token
from sqlalchemy import update, insert
from routers.userposts import userposts_router

router = APIRouter(
  prefix="/follows",
  tags=["follows"]
);

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


@router.post("/follow/{user_id}")
def follow_user(user_id: int,
                db: Session = Depends(get_db),
                current_user = Depends(get_current_user)
):
  print(current_user['id'])
  if current_user["id"] == user_id:
    raise HTTPException(status_code=400, detail="You can't follow yourself");
  
  target_user = db.query(UserModel).filter(UserModel.id == user_id).first()
  if not target_user:
    raise HTTPException(status_code=404, detail="User Not Found");
  
  
  stmt = insert(followers).values(
      follower_id=current_user['id'],
      followed_id=user_id
  )
  db.execute(stmt)
  db.commit()
  return {"msg":"followed"}
  
