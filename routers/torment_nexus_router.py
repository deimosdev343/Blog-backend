from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, func, case
from models.post_model import Post, PostVote
from models.user_model import UserModel, followers
from routers.userposts import userposts_router
from database import SessionLocal
from dto.suggest_text_dto import SuggestTextInput

from utils.auth_scheme import get_current_user
from openai import OpenAI

router = APIRouter(
  prefix="/ai",
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/suggests")
def get_suggestions():
  return ""