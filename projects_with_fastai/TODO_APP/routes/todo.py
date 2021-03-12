import fastapi
from fastapi import Depends, status

from typing import List, Dict

from sqlalchemy.orm import Session

from ..models import schemas, models
from ..database import get_db, get_current_user
from ..crud import todo


router = fastapi.APIRouter(
    prefix="/todos",
    tags=['Blogs']
)


# get todos
@router.get("/api/mytodos", response_model=List[schemas.TODO])
def get_own_todos(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """return a list of TODOs owned by current user"""
    return todo.get_user_todos(current_user.id, db)


# add to do
@router.post("/api/todos", response_model=schemas.TODO)
def add_a_todo(todo_data: schemas.TODOCreate, current_user: models.User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    """add a TODO"""
    return todo.create_todo(db, current_user, todo_data)


# delete a todo
@router.delete('/{id}', name="delete_blog", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return todo.delete_todo(id, db)


# update a todo
@router.put("/api/todos/{todo_id}", response_model=schemas.TODO, status_code=status.HTTP_202_ACCEPTED)
def update_a_todo(todo_id: int, todo_data: schemas.TODOUpdate, current_user: models.User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    return todo.update_todo(todo_id, db, todo_data)


# get a blog with blog id
@router.get('/{id}', name='show_blog', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
async def show_todo(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)) -> Dict:
    return todo.get_todo(id, db)
