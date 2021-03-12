import fastapi
from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from datetime import timedelta

from ..models import models, schemas
from ..database import get_db
from ..hashing import Hash
from ..crud import user
from ..token import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES


router = fastapi.APIRouter(
    prefix="/api/",
    tags=['Authentication']
)


def authenticate_user(db, email: str, password: str):
    user_ = user.get_user_by_email(db, email)
    if not user_:
        details = "Incorrect Credentials, Check email and password"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=details)
    if not Hash.verify_password(password, user.hashed_password):
        details = "Incorrect Credentials, Check email and password"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=details)
    return user


@router.post("/token", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """generate access token for validation credentials"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password",
                            headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/login', name="login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == (request.username).lower()).first()
    if not user:
        details = "Incorrect Credentials, Check email and password"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=details)
    if not Hash.verify_password(user.password, request.password):
        details = "Incorrect Credentials, Check email and password"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=details)

    # generate a jwt token and return it
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
