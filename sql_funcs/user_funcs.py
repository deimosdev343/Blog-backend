from sqlalchemy import select, or_
from models.user_model import UserModel
from sqlalchemy.orm import Session

async def user_exists(session: Session, username: str, email:str):
  stmt = select(UserModel).where(
    or_(UserModel.username == username, UserModel.email == email)
  )
  result = await Session.execute(stmt)
  return result.scalar_one_or_none() is not None
