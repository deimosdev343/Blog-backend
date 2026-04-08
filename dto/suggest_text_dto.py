from pydantic import BaseModel

class SuggestTextInput(BaseModel):
    post: str