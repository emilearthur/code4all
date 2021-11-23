from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from app.models import schemas, models
from app.hashing import Hash


async def get_user_email(email: str, db: Session):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        details = f"{email} already exist"
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=details)
    return user


async def get_user_email_auth(email: str, db: Session):
    return db.query(models.User).filter(models.User.email == email).first()


async def authenicate_user(db: Session, email: str, password: str) -> schemas.User:
    user = await get_user_email(email, db)
    if not user:
        return False
    if not Hash.verify_password(password, user.hashed_password):
        return False
    return user


async def create_user(user_data: schemas.UserCreate, db: Session):
    """ADD new user"""
    new_user = await get_user_email(user_data.email, db)
    if new_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"{user_data.email} already registereed")

    new_user = models.User(lname=(user_data.lname).lower(),
                           fname=(user_data.fname).lower(),
                           email=(user_data.email).lower(),
                           password=Hash.get_password_hash(user_data.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def show_user(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        details = "User not found"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=details)
    return user


def user_right(current_user_id: int, user_id: int):
    if current_user_id != user_id:
        return True
    return False
