import bcrypt

def hash_password(password: str) -> str:
  hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
  return hashed.decode("utf-8")

def verify_password(cleartxt_pw, hashed_pw):
  if isinstance(hashed_pw, str):
    hashed_pw = hashed_pw.encode("utf-8")
  return bcrypt.checkpw(cleartxt_pw.encode("utf-8"), hashed_pw)
