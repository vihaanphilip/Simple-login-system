from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

#to run type:
#uvicorn main:app --reload

app = FastAPI()

# Set up CORS middleware to enable cross-origin requests
origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

def check_credentials(user: User, db: Session = Depends(get_db)):
    user_model = db.query(models.User).filter(models.User.username == user.username).first()
    if user_model is None:
        return False
    if user_model.password != user.password:
        return False
    return True

@app.post("/login")
def login(user: User, db: Session = Depends(get_db)):
    if check_credentials(user, db):
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Login unsuccessful")




