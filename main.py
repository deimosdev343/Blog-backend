from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from routers import user_router, post_router, follow_router, vote_router
from database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from utils.limiter import limiter

from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.extension import _rate_limit_exceeded_handler
load_dotenv()

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
app.include_router(user_router.router)
app.include_router(post_router.router)
app.include_router(follow_router.router)
app.include_router(vote_router.router)

@app.get("/")
def root():
    return {"message":"Backend API"}