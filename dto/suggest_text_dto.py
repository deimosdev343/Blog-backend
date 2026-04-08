from pydantic import BaseModel

class PostInput(BaseModel):
    post: str