from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, func, case
from models.post_model import Post, PostVote
from models.user_model import UserModel, followers
from routers.userposts import userposts_router
from database import SessionLocal
from dto.suggest_text_dto import SuggestTextInput, ExpandSuggestInput
from config import TORMENT_NEXUS_KEY
from utils.auth_scheme import get_current_user
from openai import OpenAI
import yake
import json


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

def detect_tone(text):
    """Detect writing style and emotional tone"""
    tone_indicators = {
        "academic": ["furthermore", "moreover", "consequently", "thus", "therefore"],
        "casual": ["you know", "like", "actually", "honestly", "anyway"],
        "persuasive": ["must", "should", "clearly", "obviously", "undoubtedly"],
        "storytelling": ["once", "suddenly", "meanwhile", "eventually", "finally"],
        "technical": ["algorithm", "data", "analysis", "process", "system"]
    }
    detected = {tone: sum(1 for word in indicators if word in text.lower()) 
                for tone, indicators in tone_indicators.items()}
    return max(detected, key=detected.get) if any(detected.values()) else "neutral"

def extract_keywords(text):
    kw_extractor = yake.KeywordExtractor(top=5)
    keywords = kw_extractor.extract_keywords(text)
    return [kw for kw, score in keywords]


@router.post("/suggests/v2")
def get_suggestions_v2(data: SuggestTextInput): 
  if not data.post.strip():
     raise HTTPException(status_code=400, detail="The post is empty")
  
  
  tail = data.post[-2500:]
  
  keywords = extract_keywords(tail);
  keywords_str = ", ".join(keywords)
  tone = detect_tone(data.post)
  
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
    
    
    CONTEXT ANALYSIS:
    - Tone: {tone}
    - context Keywords: {keywords_str}
    
    
    Return JSON:
    {{ "suggestions": ["...", "...", "..."] }}


    Post:
    "{tail}"
  """
  try:
    response = client.chat.completions.create(
      model="gpt-4o",
      messages=[{"role": "user", "content": prompt}],
      response_format={"type": "json_object"},
      temperature=0.8
    )
    print(response.choices[0].message.content)
    return json.loads(response.choices[0].message.content)  
  except Exception as e:
    print(e)
    raise HTTPException(status_code=500, detail="API Unavaliable")

@router.post("/expand")
def get_expand(data: ExpandSuggestInput):
  tail = data.post[-2500:]
  
  if not data.post.strip():
     raise HTTPException(status_code=400, detail="The post is empty")
  if not data.suggestion.strip():
     raise HTTPException(status_code=400, detail="The suggestion is empty")
   
  keywords = extract_keywords(tail);
  keywords_str = ", ".join(keywords)
  tone = detect_tone(data.post)
  
  prompt = f"""
    You are helping a writer expand on a suggestion they liked.
    
    ORIGINAL POST CONTEXT (last part):
    "{tail}"
    
    SUGGESTION THEY WANT TO EXPAND:
    "{data.suggestion}"
    
    KEYWORDS:
    "{keywords_str}"
    
    Write 2-4 sentences that naturally extend from the suggestion.
    - Match the tone and style of the original post
    - Don't repeat the suggestion verbatim
    - End in a way that the user could continue from
    
    Return JSON:
    {{
        "expanded_text": "...",
    }}
    """
  try:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.7
    )
    
    result = json.loads(response.choices[0].message.content)
    
    return result
    
  except Exception as e:
    print(e)
    raise HTTPException(status_code=500, detail="Expansion API unavailable")
  