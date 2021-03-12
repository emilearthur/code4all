import os
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from token import decode_access_token, oauth2_scheme


# creating db connection
SQLALCHEMY_DB_URL = os.environ['SQLALCHEMY_DATABASE_URL']
# engine = create_engine(SQLALCHEMY_DB_URL)

SQLALCHAMY_DATABASE_URL = 'sqlite:///./blog.db'
engine = create_engine(SQLALCHAMY_DATABASE_URL, connect_args={"check_same_thread": False})


SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return decode_access_token(db, token)
