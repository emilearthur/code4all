
from datetime import timedelta

from typing import List
import os
import fastapi
from fastapi import Depends, status, HTTPException

from fastapi.security.oauth2 import OAuth2PasswordRequestForm,  OAuth2PasswordBearer
from sqlalchemy.orm.session import Session

from .models import models, schemas
from .database import engine, get_db
from .crud import user, todo
from .routes.authentication import authenticate_user

from .routes.user import get_current_user


app = fastapi.FastAPI()

ACCESS_TOKEN_EXPIRE_MINUTES = os.environ['ACCESS_TOKEN_EXPIRE_MINUTES']

@app.post("/api/users", name="signup",  response_model=schemas.User)
def signup(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """ADD new user"""
    user = user.get_user_by_email(db, user_data.email)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"{user_data.email} already registereed")
    
    signedup_user = user.create_user(db, user_data) 
    return signedup_user


@app.post("/api/token", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """generate access token for validation credentials"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Incorrect email or password", 
                            headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)








@app.get("/api/mytodos", response_model=List[schemas.TODO])
def get_own_todos(current_user: models.User = Depends(get_current_user), db: Session=Depends(get_db)):
    """return a list of TODOs owned by current user"""
    todos = todo.get_user_todos(current_user.id, db)
    return todos


@app.post("/api/todos", response_model=schemas.TODO)
def add_a_todo(todo_data: schemas.TODOCreate, 
               current_user: models.User = Depends(get_current_user), 
               db: Session = Depends(get_db)):
    """add a TODO"""
    todo = todo.create_todo(db, current_user, todo_data)


@app.put("/api/todos/{todo_id}", response_model=schemas.TODO)
def update_a_todo(todo_id: int, 
                  todo_data: schemas.TODOUpdate, 
                  current_user: models.User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    todo = todo.get_todo(db, todo_id)
    updated_todo = todo.update_todo(db, todo_id, todo_data)
    return updated_todo
