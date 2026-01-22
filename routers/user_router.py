from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dto.user_dto import UserCreate, UserLogin
from models.user_model import UserModel
from database import SessionLocal

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
    
@router.get('/test')
def test(db: Session = Depends(get_db)):
  return {"msg":"test route"};