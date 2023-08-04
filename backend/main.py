from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

#jwt
import jwt
import time
from typing import Dict

JWT_SECRET = 'myjwtsecret'
JWT_ALGORITHM = 'HS256'

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

class Token(BaseModel):
    access_token: str

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

# Post login
@app.post("/login")
def login(user: User, db: Session = Depends(get_db)):
    if check_credentials(user, db):
        return signJWT(user.username)
    else:
        raise HTTPException(status_code=404, detail="Invalid credentials")

# Post verify
@app.post("/verify")
def login(jwtoken: Token):
    if verify_jwt(jwtoken.access_token):
        return {"message": "Valid"}
    else:
        return {"message": "Invalid"}



def check_credentials(user: User, db: Session = Depends(get_db)):
    user_model = db.query(models.User).filter(models.User.username == user.username).first()
    if user_model is None:
        return False
    if user_model.password != user.password:
        return False
    return True

############################
# Auth Handler Functions
############################

def token_response(token: str, username: str):
    return {
        "access_token": token,
        "username": username
    }

# function used for signing the JWT string
def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token, user_id)

# function used for decoding the JWT string
def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
    
# function used for verifying the JWT string
def verify_jwt(jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid
