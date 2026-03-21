from pydantic import BaseModel


class VoteDto(BaseModel):
  post_id: int
  content: str
  