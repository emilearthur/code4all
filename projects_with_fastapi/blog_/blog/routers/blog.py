
import fastapi
from fastapi import Depends, status

from typing import List, Dict

from sqlalchemy.orm import Session

from ..models import schemas, models
from ..database import get_db
from ..crud import blog
from ..oauth2 import get_current_user


router = fastapi.APIRouter(
    prefix="/blog",
    tags=['Blogs']
)



# get all blogs in db
@router.get('/', name='all_blogs', response_model=List[schemas.ShowBlog])
async def blogs_all(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)) -> List:
    return blog.get_all(db)


# create a blog
@router.post('/', name='create_blog', status_code=status.HTTP_201_CREATED)
async def create(request: schemas.BlogBase, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)) -> models.Blog:
    return blog.create(request, db)


# delete a blog
@router.delete('/{id}', name="delete_blog", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blog.destroy(id, db)


# update blog
@router.put('/{id}',  name="update_blog", status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, request: schemas.BlogBase, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blog.update(id, request, db)


# get a blog with blog id
@router.get('/{id}', name='show_blog', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
async def show_blog(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)) -> Dict:
    return blog.get_blog(id, db)