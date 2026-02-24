from pydantic import BaseModel

class FollowUser(BaseModel):
  follow_user_id:str
  
