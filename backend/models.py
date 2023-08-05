from sqlalchemy import Column, Integer, String, Float
from database import Base_1, Base_2

class User(Base_1):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)

class Login(Base_2):
    __tablename__ = "logins"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    time = Column(String)