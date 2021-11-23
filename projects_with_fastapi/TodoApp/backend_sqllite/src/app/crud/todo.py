from fastapi import HTTPException, status, Response, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session
from app.database import get_current_user
from app.models import models, schemas
from app.crud.user import user_right


async def create_todo(todo_data: schemas.TODOCreate, db: Session,
                      current_user: models.User = Depends(get_current_user)):
    todo = models.TODO(text=todo_data.text,
                       completed=todo_data.completed,
                       priority=todo_data.priority)
    todo.owner = current_user
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


async def delete_todo(id: int, db: Session, current_user: schemas.User):
    todo = db.query(models.TODO).filter(models.TODO.id == id).first()
    if not todo:
        detail = f"Todo {id} not found in db, thus cannot deleted"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    if user_right(todo.owner_id, current_user.id):
        detail = "Unauthorized to delete, kindly login into your Account"
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
    db.delete(todo)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


async def update_todo(id: int, db: Session, todo_data: schemas.TODOUpdate, current_user: schemas.User):
    todo = db.query(models.TODO).filter(models.TODO.id == id)
    if not todo.first():
        detail = f"Todo {id} not found in db, thus cannot updated"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    if user_right(todo.first().owner_id, current_user.id):
        detail = "Unauthorized to Update, kindly login into your Account"
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

    todo.update({'text': todo_data.text,
                 'completed': todo_data.completed,
                 'priority': todo_data.priority},
                synchronize_session=False)

    db.commit()
    # db.refresh(todo)
    # return todo
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=f"todo {id} has been updated")


async def get_user_todos(userid: int, db: Session):
    return db.query(models.TODO).filter(models.TODO.owner_id == userid).all()


async def get_todo(id: int, db: Session):
    todo = db.query(models.TODO).filter(models.TODO.id == id).first()
    if not todo:
        # response.status_code = status.HTTP_404_NOT_FOUND
        details = f"Todo {todo} not found"
        # return data
        # return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=data)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=details)
    return todo
