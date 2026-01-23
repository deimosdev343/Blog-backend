from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):
  data_to_encode = data
  expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  data_to_encode.update({"exp": expire})
  return jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
  try:
    payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
    return payload
  except JWTError:
    return None

.