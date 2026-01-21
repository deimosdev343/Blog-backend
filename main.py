from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

@app.get("/")
def root():
    return {"message":"Backend API"}