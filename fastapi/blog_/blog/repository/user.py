from fastapi import Depends, status, HTTPException


from sqlalchemy.orm import Session

from ..models import schemas, models
from ..database import get_db
from ..hashing import Hash


def create(request: schemas.User, db: Session):
    new_user = models.User(name = request.name,
                           email = request.email, 
                           password = Hash.bcryt(request.password))
    db.add(new_user) 
    db.commit()
    db.refresh(new_user)
    return new_user


def show_user(id: int,  db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        details = f"User not found"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=details)
    return user