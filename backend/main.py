from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import models
from database import engine_1, SessionLocal_1, engine_2, SessionLocal_2
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

models.Base_1.metadata.create_all(bind=engine_1) #create the users database
models.Base_2.metadata.create_all(bind=engine_2) #create the logins database

def get_users_db():
    try:
        db = SessionLocal_1()
        yield db
    finally:
        db.close()

def get_logins_db():
    try:
        db = SessionLocal_2()
        yield db
    finally:
        db.close()

class User(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1, max_length=100)

class Token(BaseModel):
    access_token: str

class Login(BaseModel):
    username: str

###
# Handle logins database
####

@app.get("/logins")
def read_api(db: Session = Depends(get_logins_db)):
    return db.query(models.Login).all()

@app.post("/logins")
def create_login(login: Login, db: Session = Depends(get_logins_db)):
    login_model = models.Login()
    login_model.username = login.username
    login_model.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    db.add(login_model)
    db.commit()

    return {"message": "Login recorded"}


###
# Handle users database
####

@app.get("/users")
def read_api(db: Session = Depends(get_users_db)):
    return db.query(models.User).all()

@app.post("/users")
def create_user(user: User, db: Session = Depends(get_users_db)):
    user_model = models.User()
    user_model.username = user.username
    user_model.password = user.password

    if user_model.username == "" or user_model.password == "":
        raise HTTPException(
            status_code=400, detail="Username or password cannot be empty"
        )

    if db.query(models.User).filter(models.User.username == user_model.username).first():
        raise HTTPException(
            status_code=400, detail="Username already exists"
        )

    db.add(user_model)
    db.commit()

    return signJWT(user_model.username)

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_users_db)):
    # counter = 0

    # for x in BOOKS:
    #     counter += 1
    #     if x.id == book_id:
    #         del BOOKS[counter-1]
    #         return {"message": "Deleted book"}

    user_model = db.query(models.User).filter(models.User.id == user_id).first()

    if user_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {user_id} not found"
        )
    
    db.query(models.User).filter(models.User.id == user_id).delete()

    db.commit()

# Post login
@app.post("/login")
def login(user: User, db: Session = Depends(get_users_db)):
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

def check_credentials(user: User, db: Session = Depends(get_users_db)):
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
        "expires": time.time() + 60
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
