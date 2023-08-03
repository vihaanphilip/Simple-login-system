from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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
        return JSONResponse(content = {"error": "Invalid username"}, status_code=404)
    if user_model.password != user.password:
        return JSONResponse(content={"error": "Password mismatch"}, status_code=404)
    return JSONResponse(content = {"username": user_model.username, "password": user_model.password})

@app.post("/login")
def login(user: User, db: Session = Depends(get_db)):
    response =  check_credentials(user, db)
    if response.status_code == 200:
        return response
    else:
        raise HTTPException(status_code=response.status_code, detail="Invalid credentials")




