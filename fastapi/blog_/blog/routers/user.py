import fastapi
from fastapi import Depends, status, HTTPException


from sqlalchemy.orm import Session

from ..models import schemas, models
from ..database import get_db
from ..hashing import Hash

router = fastapi.APIRouter()

# creating a user 
@router.post('/user', name="create_user", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser, tags=['users'])
async def create_user(user: schemas.User, db: Session = Depends(get_db)) -> models.User:
    new_user = models.User(name = user.name,
                           email = user.email, 
                           password = Hash.bcryt(user.password))
    db.add(new_user) 
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/user/{id}', name="get_user", response_model=schemas.ShowUser, tags=['users'])
def get_user(id: int,  db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        details = f"User not found"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=details)
    return user