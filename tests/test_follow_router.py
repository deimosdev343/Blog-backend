import pytest
from sqlalchemy import select
 
from models.user_model import followers
 
 
def _follows(db_session, follower, followed):
    row = db_session.execute(
        select(followers).where(
            followers.c.follower_id == follower.id,
            followers.c.followed_id == followed.id,
        )
    ).first()
    return row is not None


class TestFollow:
  def test_follow(
    self,auth_client, make_user,db_session
  ):
    vasyan = make_user(username="vasyan")
    arnold = make_user(username="arnie")
    
    response = auth_client(vasyan).post(
      "/follow/", json={"follow_user_id": str(arnold.id)}
    )
    assert response.status_code == 200
    assert _follows(db_session,vasyan, arnold) is True
  def test_following_directional(
    self,auth_client, make_user,db_session
  ):
    vasyan = make_user(username="vasyan")
    arnold = make_user(username="arnie")
    response = auth_client(vasyan).post(
      "/follow/", json={"follow_user_id": str(arnold.id)}
    )
    assert response.status_code == 200
    assert _follows(db_session, arnold, vasyan) is False
    