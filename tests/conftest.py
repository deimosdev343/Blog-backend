import os
TEST_DATABASE_URL = "sqlite+pysqlite:///:memory:"

os.environ["DATABASE_URL"] = TEST_DATABASE_URL
os.environ["SECRET_KEY"] = "test-secret-key-not-used-in-production"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "60"
os.environ["OPEN_AI_KEY"] = "test-openai-key"

import pytest 
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base 
from main import app 
from models.post_model import Post, PostComment, PostVote
from models.user_model import UserModel, followers

from routers import (
  comment_router,
  follow_router,
  llm_router,
  post_router,
  user_router,
  vote_router
)

from routers.user_router import userposts_router
from utils import auth_scheme
from utils.hash import hash_password
from utils.limiter import limiter

TEST_ENGINE = create_engine(
  TEST_DATABASE_URL,
  connect_args={"check_same_thread": False},
  poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
  bind=TEST_ENGINE, autoflush=False, autocommit=False
)

@event.listens_for(TEST_ENGINE, "connect")
def _enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

def _override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


_DB_DEPENDENCIES = (
    user_router.get_db,
    post_router.get_db,
    follow_router.get_db,
    vote_router.get_db,
    comment_router.get_db,
    llm_router.get_db,
    userposts_router.get_db,
)

@pytest.fixture(autouse=True)
def _fresh_schema():
    Base.metadata.create_all(bind=TEST_ENGINE)
    yield
    Base.metadata.drop_all(bind=TEST_ENGINE)

    