from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from models.post_model import Post, PostVote
from database import SessionLocal
from utils.auth_scheme import get_current_user, blacklist_token
from sqlalchemy import update, insert, delete, select, func
from dto.vote_dto import VoteDto

router = APIRouter(
  prefix="/vote"
)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@router.post("/")
def vote(
  new_vote: VoteDto,
  db: Session = Depends(get_db),
  user = Depends(get_current_user)
):
  post = db.query(Post).filter(Post.id == new_vote.post_id).first()
  if not post:
    raise HTTPException(status_code=404, detail="Post not found")
  stmt = select(PostVote).where(
      PostVote.user_id == user["id"],
      PostVote.post_id == new_vote.post_id
  )
  existing_vote = db.execute(stmt).scalar_one_or_none()  
  if existing_vote:
    db.delete(existing_vote)
    if existing_vote.vote == new_vote.vote:
      db.commit()
      return {"msg":"vote successfully removed"}
  db.add(PostVote(
    user_id = user["id"],
    post_id = new_vote.post_id,
    vote = new_vote.vote
  ))
  db.commit()
  return {"msg":"vote updated"};  
  