import fastapi
from fastapi import Depends, status


from sqlalchemy.orm import Session

from ..models import schemas, models
from ..database import get_db


from ..crud import user

router = fastapi.APIRouter(
    prefix="/user",
    tags=['Users']
)

# creating a user 
@router.post('/', name="create_user", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
async def create_user(request: schemas.User, db: Session = Depends(get_db)) -> models.User:
    return await user.create(request, db)


@router.get('/{id}', name="show_user_id", response_model=schemas.ShowUser)
async def get_user(id: int,  db: Session = Depends(get_db)):
    return await user.show_user(id, db)

