import jwt
import os
from datetime import timedelta, datetime

from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status

from sqlalchemy.orm.session import Session

from . import schemas
from .crud import user
SECRET_KEY = os.environ['SECRET_KEY']
ALGORITHM = os.environ["ALGORITHM"]


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(db: Session, token):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenicate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except jwt.PyJWTError:
        raise credentials_exception
    user_ = user.get_user_email(email=token_data.email, db=db)
    if user_ is None:
        raise credentials_exception
    return user_


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
