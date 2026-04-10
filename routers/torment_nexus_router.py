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

def get_last_paragraphs(text, words=500):
  split_words = text.split()
  relevent_words = split_words[-words:]
  return "".join(relevent_words)
    

@router.post("/suggests")
def get_suggestions(data: SuggestTextInput):
  last_paragraphs_output = get_last_paragraphs(data.post, 500)
  print(last_paragraphs_output);
  prompt = f"""
    You are a writing assistant helping a user continue their article.

    Given the text below, generate 3 distinct suggestions for what the writer could write next.

    Guidelines:
    - Each suggestion should be 1–2 sentences max
    - Continue naturally from the tone and topic
    - Each suggestion should take a slightly different direction (e.g. example, argument, question, contrast, or storytelling)
    - Do NOT repeat what was already written
    - Do NOT summarize
    - Do NOT write full paragraphs
    - Keep it inspiring but practical
    
    return a list 

    Post:
    "{last_paragraphs_output}"
  """
  response = client.responses.create(
      model="gpt-4o",
      input=prompt
  )
  text_output = response.output[0].content[0].text
  text_output = text_output.replace("\n\n", "\n ")
  return text_output