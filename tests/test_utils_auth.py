from datetime import datetime, timedelta, timezone
 
import pytest
from jose import jwt
 
from config import ALGORITHM, SECRET_KEY
from utils.auth import create_access_token, decode_access_token
from utils.hash import hash_password, verify_password
 
class TestPasswordHashing:
  def test_hash_not_cleartext(self):
    hashed = hash_password("hunter2")
    assert "hunter2" not in hashed 
    assert hashed.startswith("$2b$")
  def test_salted(self):
    assert hash_password("testPassword") != hash_password("testPassword")
  def test_accept_correct_password(self):
    stored = hash_password("testPass")
    assert verify_password("testPass", stored) is True
  def test_rejects_wrong_password(self):
    stored = hash_password("testPass")
    assert verify_password("testwrongpass",  stored) is False
  def test_none_ascii(self):
    stored = hash_password("тестовые_пароль")
    assert verify_password("тестовые_пароль",stored) is True


class TestAccessTokens:
  def test_preserve_claim(self):
    token = create_access_token(
      {"username":"vasyan", "email":"vasyan@ap-pro.ru", "id": 13}
    )
    payload = decode_access_token(token)
    
    assert payload["username"] == "vasyan"
    assert payload["email"] == "vasyan@ap-pro.ru"
    assert payload["id"] ==  13
  def test_token_carries_an_expiry(self):
        token = create_access_token({"username": "alice", "id": 1})
        assert "exp" in decode_access_token(token)
 
  def test_decode_returns_none_for_garbage(self):
      assert decode_access_token("not-a-token") is None

  def test_decode_rejects_a_token_signed_with_another_key(self):
      forged = jwt.encode(
          {"username": "mallory", "id": 99},
          "a-different-secret",
          algorithm=ALGORITHM,
      )
      assert decode_access_token(forged) is None
  def test_decode_rejects_an_expired_token(self):
    expired = jwt.encode(
        {
            "username": "alice",
            "id": 1,
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    assert decode_access_token(expired) is None
