from ..models import models, schemas
from fastapi import HTTPException, status, Response, JSONResponse
from sqlalchemy.orm.session import Session


def create_todo(db: Session, current_user: models.User, todo_data: schemas.TODOCreate):
    todo = models.TODO(text=todo_data.text,
                       completed=todo_data.compeleted,
                       priority=todo_data.priority)
    todo.owner = current_user
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def update_todo(id: int, db: Session, todo_data: schemas.TODOUpdate):
    todo = db.query(models.TODO).filter(models.TODO.id == id)
    if not todo.first():
        detail = f"todo {id} not found in db, thus cannot updated"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

    todo.update({'text': todo_data.text,
                 'completed': todo_data.compeleted},
                synchronize_session=False)

    db.commit()
    # db.refresh(todo)
    # return todo
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=f"todo {id} has been updated")


def delete_todo(id: int, db: Session):
    todo = db.query(models.TODO).filter(models.TODO.id == id)
    if not todo.first():
        detail = f"todo {id} not found in db, thus cannot deleted"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    db.delete(todo)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def get_user_todos(userid: int, db: Session):
    return db.query(models.TODO).filter(models.TODO.owner_id == userid).all()


def get_todo(id: int, db: Session):
    todo = db.query(models.TODO).filter(models.TODO.id == id).first()
    if not todo:
        # response.status_code = status.HTTP_404_NOT_FOUND
        details = f"Blog {todo} not found"
        # return data
        # return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=data)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=details)
    return todo
