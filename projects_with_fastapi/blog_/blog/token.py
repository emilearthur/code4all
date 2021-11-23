import datetime
from typing import Optional
from datetime import timedelta, datetime

from jose import jwt, JWTError

from blog.models.schemas import TokenData

# to get a string like this run:
# openssl rand -hex 32

SECRET_KEY = "951bd710e86d6ef6b122411730f63cb9039c53a4ca1f3331db0d21476ef6178f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire}) 
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    
        token_data = TokenData(username=email)
    except JWTError:
        raise credentials_exception