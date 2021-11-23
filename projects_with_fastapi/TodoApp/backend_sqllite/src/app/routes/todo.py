import fastapi
from fastapi import Depends, status, Response
from fastapi.responses import JSONResponse

from typing import List, Dict

from sqlalchemy.orm import Session

from app.models import schemas, models
from app.database import get_db, get_current_user
from app.crud import todo


router = fastapi.APIRouter()


# get todos
@router.get("/", response_model=List[schemas.TODO], status_code=status.HTTP_200_OK)
async def get_own_todos(current_user: models.User = Depends(get_current_user),
                        db: Session = Depends(get_db)) -> List:
    """return a list of TODOs owned by current user"""
    return await todo.get_user_todos(current_user.id, db)


# add to do
@router.post("/", response_model=schemas.TODO, status_code=status.HTTP_201_CREATED)
async def add_a_todo(todo_data: schemas.TODOCreate, current_user: models.User = Depends(get_current_user),
                     db: Session = Depends(get_db)) -> schemas.TODO:
    """add a TODO"""
    return await todo.create_todo(todo_data, db, current_user)


# delete a todo
@router.delete('/{id}', name="delete_todo", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(id: int, db: Session = Depends(get_db),
                  current_user: schemas.User = Depends(get_current_user)) -> Response:
    return await todo.delete_todo(id, db, current_user)


# update a todo
@router.put('/{todo_id}', name="update_todo", status_code=status.HTTP_202_ACCEPTED)
async def update_a_todo(todo_id: int, todo_data: schemas.TODOUpdate,
                        current_user: schemas.User = Depends(get_current_user),
                        db: Session = Depends(get_db)) -> JSONResponse:
    return await todo.update_todo(todo_id, db, todo_data, current_user)


# get a todo with blog todo id
@router.get('/{id}', name='show_blog', response_model=schemas.TODO, status_code=status.HTTP_200_OK)
async def show_todo(id: int, db: Session = Depends(get_db),
                    current_user: schemas.User = Depends(get_current_user)) -> Dict:
    return await todo.get_todo(id, db)
