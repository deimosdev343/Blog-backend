from pydantic import BaseModel
from typing import Literal

class VoteDto(BaseModel):
  vote: Literal[-1, 1]
  post_id: int