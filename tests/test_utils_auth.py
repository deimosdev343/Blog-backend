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
  def test_salted(self):
    assert hash_password("testPassword") != hash_password("testPassword")
  def test_accept_correct_password(self):
    stored = hash_password("testPass").decode("utf-8")
    assert verify_password("testPass", stored) is True
  def test_rejects_wrong_password(self):
    stored = hash_password("testPass").decode("utf-8")
    assert verify_password("testwrongpass",  stored) is False
  def test_none_ascii(self):
    stored = hash_password("тестовые_пароль").decode("utf-8")
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
