from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, func, case
from models.post_model import Post, PostVote
from models.user_model import UserModel, followers
from routers.userposts import userposts_router
from database import SessionLocal
from dto.suggest_text_dto import SuggestTextInput
from config import TORMENT_NEXUS_KEY
from utils.auth_scheme import get_current_user
from openai import OpenAI

router = APIRouter(
  prefix="/ai",
)
client = OpenAI(api_key=TORMENT_NEXUS_KEY)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/suggests")
def get_suggestions(data: SuggestTextInput):
  prompt = f"""
  Generate 3 short, natural, and engaging social media reply comments 
  to the following post. Keep them casual and varied in tone.

  Post:
  "{data.post}"

  Return as a JSON array of strings.
  """
  response = client.responses.create(
      model="gpt-4o",
      input=prompt
  )
  text_output = response.output[0].content[0].text
  try:
    import json
    suggestions = json.loads(text_output)
  except:
    # fallback if model didn't return valid JSON
    suggestions = [line.strip("- ").strip() for line in text_output.split("\n") if line.strip()]

  return {"suggestions": suggestions}