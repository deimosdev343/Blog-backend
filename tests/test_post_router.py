from datetime import datetime, timedelta
from types import SimpleNamespace
 
import pytest
 
from models.post_model import Post, PostVote
 
BASE_TIME = datetime(2026, 1, 1, 12, 0, 0)

class TestCreatePost:
  def test_create_post(
    self, auth_client, make_user,db_session
  ):
    user = make_user(username="user")
    response = auth_client(user).post(
      "/posts", json={"title":"hello", "content":"test"}
    )
    assert response.status_code == 200
    post = db_session.query(Post).one()
    assert post.title == "hello"
    assert post.content == "test"
    assert post.author_id == user.id
  
  def test_post_contains_user_data(
    self, auth_client, make_user,db_session
  ):
    
    user = make_user(username="user", avatar_url="https://fakeimages.com/1.jpg")
    response = auth_client(user).post(
      "/posts", json={"title":"hello", "content":"test"}
    )
    post = db_session.query(Post).one()
    assert post.username == "user"
    assert post.user_avatar == "https://fakeimages.com/1.jpg"
    
  def test_rejects_missing_field(
    self, auth_client, make_user
  ):
    user = make_user(username="user")
    response = auth_client(user).post("/posts/", json={"title":"hello"})
    
    assert response.status_code == 422  

class TestListPosts:
  def test_no_posts_handle(self, client):
    response = client.get("/posts")
    assert response.status_code == 200
    assert response.json() == []
  def test_get_votes_of_post(
    self, client, make_user, make_post, db_session
  ):
    user = make_user(username="user")
    second_user = make_user(username="user2")
    third_user = make_user(username="user3")
    post = make_post(user)
    db_session.add_all(
        [
            PostVote(user_id=user.id, post_id=post.id, vote=1),
            PostVote(user_id=second_user.id, post_id=post.id, vote=1),
            PostVote(user_id=third_user.id, post_id=post.id, vote=-1),
        ]
    )
    db_session.commit()

    body = client.get("/posts/").json()[0]

    assert body["upvotes"] == 2
    assert body["downvotes"] == 1

    
    
    
