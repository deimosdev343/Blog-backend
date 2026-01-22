import bcrypt

def hash_password(password: str):
  encoded_password = password.encode("utf-8")
  return bcrypt.hashpw(encoded_password,bcrypt.gensalt());

def verify_password(cleartxt_pw, hashed_pw):
  encoded_cleartxt = cleartxt_pw.encode("utf-8")
  encoded_hashed = hashed_pw.encode("utf-8")
  return bcrypt.checkpw(encoded_cleartxt, encoded_hashed)
