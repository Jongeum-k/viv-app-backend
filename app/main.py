from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.routers.words import router as words_router

from app.db import get_db

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(words_router)

@app.get("/")
def read_root():
    return {"message": "Howdy, cowboy. FastAPI is up and runnin"}



@app.get("/health/db")
def check_db(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1 AS ok"))
        row = result.fetchone()
        return {
            "status": "ok",
            "database": "connected",
            "data": row.ok,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(e)}",
        )