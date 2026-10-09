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
    
  
    
    
    
