from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from dto.user_dto import UserCreate, UserLogin, updateAvatar, updateUserDetails
from models.user_model import UserModel
from models.post_model import Post
from database import SessionLocal
from utils.hash import hash_password, verify_password
from utils.auth import create_access_token
from utils.auth_scheme import get_current_user, blacklist_token
from sqlalchemy import update
from routers.userposts import userposts_router
from routers.follows import follow_router;
from utils.limiter import limiter
router = APIRouter(
  prefix="/user",
  tags=["user"]
)


router.include_router(userposts_router.router)



def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
    

@router.get('/auth')
def auth(user = Depends(get_current_user)):
  return user;

@router.get('/logout')
def logout(user = Depends(blacklist_token)):
  return {"msg":"logged out successfully"};  

@router.post('/register')
def register(user: UserCreate, db: Session = Depends(get_db)):
  existing_user = db.query(UserModel).filter(UserModel.username == user.username).first()
  if existing_user:
    raise HTTPException(status_code=400, detail="Username already exists")
  existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()
  if existing_user:
    raise HTTPException(status_code=400, detail="email already exists")
  hashed_pw = hash_password(user.password)
  db_user = UserModel(username=user.username, hashed_password=hashed_pw, email= user.email)
  db.add(db_user)
  db.commit()
  db.flush()
  return {"msg":"user successfully registered"};

@router.post("/login")
@limiter.limit("5/minute")
def login(request, user_login:UserLogin, db: Session = Depends(get_db)):
  user = db.query(UserModel).filter(UserModel.username == user_login.username).first()
  if not user: 
    raise HTTPException(status_code=401, detail="Invalid username or password")
  verify_result = verify_password(cleartxt_pw=user_login.password, hashed_pw=user.hashed_password)
  if not verify_result:
    raise HTTPException(status_code=401, detail="invalid username or password")
  
  token = create_access_token({"username":user.username, "email":user.email, "id": user.id})
  return {
    "access_token":token,
    "token_type":"bearer",
    "user_data": {"username":user.username, "email":user.email, "id": user.id}
  }


def update_avatar_in_posts(user_id, avatar_url, db: Session):
  stmt = (update(Post)
          .where(Post.author_id == user_id)
          .values(user_avatar= avatar_url))
  db.execute(stmt)
  db.commit()

@router.get("/{user_id}")
def get_specific_user(
  user_id: int,
  db: Session = Depends(get_db)
):
  existing_user = db.query(UserModel).filter(UserModel.id == user_id).first()
  if not existing_user:
    raise HTTPException(404, "User not found")
  return {
    "username":existing_user.username,
    "avatar_url": existing_user.avatar_url,
    "description": existing_user.description
  }

  
@router.put("/update_info")
def update_info(
  user_details: updateUserDetails,
  db: Session = Depends(get_db),
  user = Depends(get_current_user)
):
  stmt = (
    update(UserModel)
    .where(UserModel.id == user["id"])
    .values(description = user_details.description)
  )
  result = db.execute(stmt)
  db.commit()
  return {"msg":"avatar updated successfully"}

@router.put("/update_avatar")
def update_avatar(
  user_avatar: updateAvatar, 
  background_tasks: BackgroundTasks,
  db: Session = Depends(get_db),
  user = Depends(get_current_user),
):
  stmt = (
    update(UserModel)
    .where(UserModel.id == user["id"])
    .values(avatar_url = user_avatar.avatar_url)
  )
  
  result = db.execute(stmt)
  db.commit()
  background_tasks.add_task(
    update_avatar_in_posts, 
    user_id = user["id"], avatar_url = user_avatar.avatar_url, 
    db=db
  )
  
  return {"msg":"avatar updated successfully"}
  
  

