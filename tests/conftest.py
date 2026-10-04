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
