import fastapi
from fastapi import Depends, status, HTTPException, Response
from fastapi.responses import JSONResponse

from typing import List, Dict
import datetime

from sqlalchemy.orm import Session

from ..models import schemas, models
from ..database import get_db


router = fastapi.APIRouter()



# get all blogs in db
@router.get('/blog', name='all_blogs', response_model=List[schemas.ShowBlog], tags=['blogs'])
async def blogs_all(db: Session = Depends(get_db)) -> List:
    blogs = db.query(models.Blog).all()
    return blogs


# create a blog
@router.post('/blog', name='create_blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
async def create(blog: schemas.BlogBase, db: Session = Depends(get_db)) -> models.Blog:
    now = datetime.datetime.now()
    new_blog = models.Blog(title=blog.title, 
                            body=blog.body, 
                            published=blog.published, 
                            created_at=now,
                            user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# delete a blog
@router.delete('/blog/{id}', name="delete_blog", status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
async def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog {id} not found in db, thus cannot deleted")
    
    blog.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update blog
@router.put('/blog/{id}',  name="update_blog", status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
async def update(id: int, request: schemas.BlogBase, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog {id} not found in db, thus cannot updated")

    now = datetime.datetime.now()
    blog.update({'title': request.title,
                 'body': request.body,
                 'published': request.published,
                 'created_at': now},
                 synchronize_session=False)
    db.commit()
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=f"blog {id} has been updated")


# get a blog with blog id
@router.get('/blog/{id}', name='show_blog', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['blogs'])
async def show_blog(id: int, response: Response, db: Session = Depends(get_db)) -> Dict:
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        details = f"Blog {id} not found"
        # return data
        #return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=data)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=details)
    return blog