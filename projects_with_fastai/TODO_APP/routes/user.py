import fastapi
from fastapi import Depends, status
from sqlalchemy.orm import Session
from ..crud import user
from ..models import schemas, models
from ..database import get_current_user, get_db

router = fastapi.APIRouter(
    prefix="/api/user",
    tags=['Users'])


@router.post("/", name="create_user", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def signup(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    return user.create_user(user_data, db)


@router.get("/{id}", name="show_user_id", response_model=schemas.User)
async def get_user(id: int, db: Session = Depends(get_db)):
    return await user.show_user(id, db)


@router.get("/me", name="read_logged_in_user", response_model=schemas.User)
def read_logged_in_user(current_user: models.User = Depends(get_current_user)):
    return current_user
