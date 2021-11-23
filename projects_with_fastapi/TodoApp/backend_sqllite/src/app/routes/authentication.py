import fastapi
from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from datetime import timedelta

from app.models import models
from app.database import get_db
from app.hashing import Hash
from app.token import create_access_token
from app.setup_environ import configure_environment


ACCESS_TOKEN_EXPIRE_MINUTES = configure_environment()[3]


router = fastapi.APIRouter(
)


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
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
