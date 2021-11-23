import jwt
from datetime import timedelta, datetime

from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status

from sqlalchemy.orm.session import Session

from app.models import schemas
from app.crud import user

from app.setup_environ import configure_environment


SECRET_KEY = configure_environment()[1]
ALGORITHM = configure_environment()[2]


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def decode_access_token(db: Session, token):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenicate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=email)
    except jwt.PyJWTError:
        raise credentials_exception
    user_ = await user.get_user_email_auth(email=token_data.username, db=db)
    if user_ is None:
        raise credentials_exception
    return user_


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
