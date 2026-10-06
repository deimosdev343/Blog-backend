import pytest
 
from models.user_model import UserModel

class TestRegister:
  def test_creates_the_user(self, client, db_session):
    response = client.post(
        "/user/register",
        json={
            "username": "alice",
            "password": "hunter2",
            "email": "alice@example.com",
        },
    )

    assert response.status_code == 200
    user = (
        db_session.query(UserModel)
        .filter(UserModel.username == "alice")
        .one()
    )
    assert user.email == "alice@example.com"

  def test_stores_hash(self, client, db_session):
    client.post(
        "/user/register",
        json={
            "username": "alice",
            "password": "hunter2",
            "email": "alice@example.com",
        },
    )

    user = db_session.query(UserModel).one()
    assert "hunter2" not in str(user.hashed_password)
    
  def test_rejects_duplicate_username(self, client, make_user):
    make_user(username="alice", email="alice@example.com")
    response = client.post(
        "/user/register",
        json={
            "username": "alice",
            "password": "different",
            "email": "someone.else@example.com",
        },
    )
    assert response.status_code == 400
    assert "username" in response.json()["detail"].lower()
    
  def test_rejects_duplicate_email(self, client, make_user):
    make_user(username="alice", email="alice@example.com")

    response = client.post(
        "/user/register",
        json={
            "username": "bob",
            "password": "hunter2",
            "email": "alice@example.com",
        },
    )

    assert response.status_code == 400
    assert "email" in response.json()["detail"].lower()

  def test_rejects_missing_field(self, client):
      response = client.post(
          "/user/register", json={"username": "alice", "password": "hunter2"}
      )
      assert response.status_code == 422

class TestLogin:
  def test_returns_token_and_user_data(self, client, make_user):
    user = make_user(username="alice", password="hunter2")
    response = client.post(
        "/user/login", json={"username": "alice", "password": "hunter2"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert body["user_data"] == {
        "username": "alice",
        "email": user.email,
        "id": user.id,
    }
  def test_the_returned_token_authenticates(self, client, make_user):
    make_user(username="alice", password="hunter2")
    token = client.post(
        "/user/login", json={"username": "alice", "password": "hunter2"}
    ).json()["access_token"]
    response = client.get(
        "/user/auth", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "alice"
  
  def test_rejects_wrong_password(self, client, make_user):
    make_user(username="alice", password="hunter2")
    response = client.post(
        "/user/login", json={"username": "alice", "password": "wrong"}
    )
    assert response.status_code == 401

  def test_register_then_login_round_trip(self, client):
    client.post(
        "/user/register",
        json={
            "username": "alice",
            "password": "hunter2",
            "email": "alice@example.com",
        },
    )

    response = client.post(
        "/user/login", json={"username": "alice", "password": "hunter2"}
    )

    assert response.status_code == 200
