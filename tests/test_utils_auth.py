from datetime import datetime, timedelta, timezone
 
import pytest
from jose import jwt
 
from config import ALGORITHM, SECRET_KEY
from utils.auth import create_access_token, decode_access_token
from utils.hash import hash_password, verify_password
 
class TestPasswordHashing:
  def test_hash_not_cleartext(self):
    hashed = hash_password("hunter2")
    assert hashed != b"hunter2"
    assert hashed.startswith(b"$2b$")
  