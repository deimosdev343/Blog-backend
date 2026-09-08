from pydantic import BaseModel, Field, model_validator
from typing import Literal, Optional

TransformAction = Literal["improve", "shorten", "expand", "grammar", "tone"]
TransformTone = Literal["professional", "casual", "confident", "plain"]

class SuggestTextInput(BaseModel):
    post: str
    
class ExpandSuggestInput(BaseModel):
    post: str
    suggestion: str

class transfromTextInput(BaseModel):
  text: str = Field(min_length=1, max_length=8000)
  action: TransformAction
  tone: Optional[TransformTone] = None
  context: str = ""
  
  @model_validator(mode="after")
  def tone_required_for_tone_action(self):
    if self.action == "tone" and self.tone is None:
      raise ValueError("Tone not provided")
    return self
    
  