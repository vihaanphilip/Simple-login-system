from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field

import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

#to run type:
#uvicorn main:app --reload

app = FastAPI()

models.Base.metadata.create_all(bind=engine) #create the database

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class User(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1, max_length=100)

@app.get("/users")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.post("/users")
def create_user(user: User, db: Session = Depends(get_db)):
    user_model = models.User()
    user_model.username = user.username
    user_model.password = user.password

    db.add(user_model)
    db.commit()

    return user



