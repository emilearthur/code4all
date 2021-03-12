from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from ..models import schemas, models
from ..hashing import Hash


async def get_user_email(email: str, db: Session):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        details = f"{email} already exist"
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=details)
    return user


# async def get_user_name(username: str, db: Session):
#     user = db.query(models.User).filter(models.User.name == username).first()
#     if user:
#         details = f"{user} already exist"
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=details)
#     return user


async def create(request: schemas.User, db: Session):
    new_user = await get_user_email(request.email, db)
    # new_user = await get_user_name(request.email, db)

    new_user = models.User(name = request.name,
                           email = (request.email).lower(), 
                           password = Hash.get_password_hash(request.password))
    db.add(new_user) 
    db.commit()
    db.refresh(new_user)
    return new_user


async def show_user(id: int,  db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        details = f"User not found"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=details)
    return user

