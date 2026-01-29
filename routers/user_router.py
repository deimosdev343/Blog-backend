from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dto.user_dto import UserCreate, UserLogin, updateAvatar
from models.user_model import UserModel
from database import SessionLocal
from utils.hash import hash_password, verify_password
from utils.auth import create_access_token
from utils.auth_scheme import get_current_user
from sqlalchemy import update
router = APIRouter(
  prefix="/user",
  tags=["user"]
)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
    

@router.get('/auth')
def auth(user = Depends(get_current_user)):
  return user;
  

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
def login(user_login:UserLogin, db: Session = Depends(get_db)):
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


@router.put("/update_avatar")
def update_avatar(
  user_avatar: updateAvatar, 
  db: Session = Depends(get_db),
  user = Depends(get_current_user)
):
  stmt = (
    update(UserModel)
    .where(UserModel.id == user["id"])
    .values(avatar_url = user_avatar.avatar_url)
  )
  result = db.execute(stmt)
  db.commit()
  return {"msg":"avatar updated successfully"}
  
  

