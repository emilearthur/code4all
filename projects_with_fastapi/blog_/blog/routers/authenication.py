import fastapi
from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from ..models import  models
from ..database import get_db
from ..hashing import Hash
from ..token import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = fastapi.APIRouter(
    tags=['Authentication']
)

@router.post('/login', name="login")
def login(request: OAuth2PasswordRequestForm= Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == (request.username).lower()).first()
    if not user:
        details = f"Incorrect Credentials, Check email and password"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=details)
    if not Hash.verify_password(user.password, request.password):
        details = f"Incorrect Credentials, Check email and password"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=details)

    # generate a jwt token and return it
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) 
    # access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}