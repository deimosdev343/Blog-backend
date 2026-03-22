from pydantic import BaseModel


class CommentDto(BaseModel):
  post_id: int
  content: str
  