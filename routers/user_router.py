from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dto.user_dto import UserCreate, UserLogin
from models.user_model import UserModel
from database import SessionLocal
from utils.hash import hash_password, verify_password
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
    

@router.get('/register')
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
  db.refresh(UserModel)

