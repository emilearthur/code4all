import datetime

from sqlalchemy.orm import Session

from ..models import models
from ..models import schemas

from fastapi import HTTPException, Response, status
from fastapi.responses import JSONResponse

def get_all(db: Session):
    blogs = db.query(models.Blog).all()

    return blogs


def create(request: schemas.BlogBase, db:Session):
    now = datetime.datetime.now()
    new_blog = models.Blog(title=request.title, 
                            body=request.body, 
                            published=request.published, 
                            created_at=now,
                            user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    
    return new_blog


def destroy(id: int, db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog {id} not found in db, thus cannot deleted")
    
    blog.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def update(id: int, request: schemas.BlogBase, db: Session):
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


def get_blog(id: int,db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        details = f"Blog {id} not found"
        # return data
        #return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=data)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=details)
    return blog