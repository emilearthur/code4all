from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.token import decode_access_token, oauth2_scheme
from app.setup_environ import configure_environment


# creating db connection
SQLALCHEMY_DB_URL = configure_environment()[0]

engine = create_engine(SQLALCHEMY_DB_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return await decode_access_token(db, token)
