from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from utils.auth import decode_access_token

auth_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

blocked_tokens: list[str] = []

def get_current_user(token: str = Depends(auth_scheme)):
  if token in blocked_tokens: 
    raise HTTPException(status_code=403, detail="Invalid or expired Token")
  payload = decode_access_token(token)
  if payload is None:
    raise HTTPException(status_code=401, detail="invalid or expired token")
  return payload

def blacklist_token(token: str = Depends(auth_scheme)):
  blocked_tokens.append(token) 

def get_current_user_if_logged_in(token: str = Depends(auth_scheme)):
  if token in blocked_tokens: 
    raise HTTPException(status_code=403, detail="Invalid or expired Token")
  payload = decode_access_token(token)
  return payload
