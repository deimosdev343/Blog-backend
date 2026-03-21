from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from models.post_model import Post, PostVote
from database import SessionLocal
from utils.auth_scheme import get_current_user, blacklist_token, get_current_user_if_logged_in
from sqlalchemy import update, insert, delete, select, func, case
