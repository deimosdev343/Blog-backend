from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from dto.user_dto import UserCreate, UserLogin, updateAvatar, updateUserDetails
from dto.folllow_dto import FollowUser
from models.user_model import UserModel, followers
from models.post_model import Post
from database import SessionLocal
from utils.hash import hash_password, verify_password
from utils.auth import create_access_token
from utils.auth_scheme import get_current_user, blacklist_token
from sqlalchemy import update, insert, delete, select, func
from routers.userposts import userposts_router

router = APIRouter(
  prefix="/follow"
  
);

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


@router.post("/")
def follow_user(follow: FollowUser,
                db: Session = Depends(get_db),
                current_user = Depends(get_current_user)
):
  
  if current_user["id"] == follow.follow_user_id:
    raise HTTPException(status_code=400, detail="You can't follow yourself");
  
  target_user = db.query(UserModel).filter(UserModel.id == follow.follow_user_id).first()
  if not target_user:
    raise HTTPException(status_code=404, detail="User Not Found");
  
  
  stmt = insert(followers).values(
      follower_id=current_user['id'],
      followed_id=follow.follow_user_id
  )
  db.execute(stmt)
  db.commit()
  return {"msg":"followed"}
  
@router.delete("/{user_id}")
def unfollow_user(
  user_id:int,
  db: Session = Depends(get_db),
  current_user = Depends(get_current_user)
):
  stmt = delete(followers).where(
    followers.c.follower_id == current_user["id"],
    followers.c.followed_id == user_id
  )
  result = db.execute(stmt)
  db.commit()
  
  return {"msg":"unfollowed"}



@router.get("/following")
def is_following(user_id: int,
  db: Session = Depends(get_db),
  current_user = Depends(get_current_user)
):

  stmt = select(followers).where(
      followers.c.follower_id == current_user["id"],
      followers.c.followed_id == user_id
  )

  return {"is_following": db.execute(stmt).first() is not None}

@router.get("/{user_id}/follow-stats")
def get_follow_stats(user_id: int, db: Session = Depends(get_db)):

    followers_count = db.execute(
        select(func.count()).where(followers.c.followed_id == user_id)
    ).scalar()

    following_count = db.execute(
        select(func.count()).where(followers.c.follower_id == user_id)
    ).scalar()

    return {
        "followers": followers_count,
        "following": following_count
    }