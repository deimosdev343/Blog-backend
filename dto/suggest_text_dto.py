from pydantic import BaseModel

class SuggestTextInput(BaseModel):
    post: str
    
class ExpandSuggestInput(BaseModel):
    post: str
    suggestion: str

