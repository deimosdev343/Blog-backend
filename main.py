from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from routers import user_router, post_router
from database import Base, engine
load_dotenv()

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router.router)
app.include_router(post_router.router)

@app.get("/")
def root():
    return {"message":"Backend API"}