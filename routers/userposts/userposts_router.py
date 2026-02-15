from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.post_model import Post 
from models.user_model import UserModel

from database import SessionLocal
from dto.post_dto import PostCreate
from utils.auth_scheme import get_current_user

router = APIRouter(
  prefix="/posts"
)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@router.get('/getPosts')
def test():
  return {"msg":"test"}