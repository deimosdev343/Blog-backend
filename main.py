from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from routers import user_router, post_router, follow_router, vote_router
from database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()

app = FastAPI()


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