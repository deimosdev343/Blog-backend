from pydantic import BaseModel, ConfigDict
from datetime import datetime

class AuthorOut(BaseModel):
  model_config = ConfigDict(from_attributes=True)
  id: int
  username: str
  avatar_url: str | None

class CommentOut(BaseModel):
  model_config = ConfigDict(from_attributes=True)
  id: int
  content: str
  created_at: datetime
  author: AuthorOut
  
class CommentListOut(BaseModel):
  comments: list[CommentOut]