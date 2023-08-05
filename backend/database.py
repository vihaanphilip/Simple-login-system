from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create database for users

SQLALCHEMY_DATABASE_URL_1 = "sqlite:///./users.db"

engine_1 = create_engine(
    SQLALCHEMY_DATABASE_URL_1, connect_args={"check_same_thread": False}
)

SessionLocal_1 = sessionmaker(bind=engine_1, autocommit=False, autoflush=False)

Base_1 = declarative_base()

# Create database for logins

SQLALCHEMY_DATABASE_URL_2 = "sqlite:///./logins.db"

engine_2 = create_engine(
    SQLALCHEMY_DATABASE_URL_2, connect_args={"check_same_thread": False}
)

SessionLocal_2 = sessionmaker(bind=engine_2, autocommit=False, autoflush=False)

Base_2 = declarative_base()