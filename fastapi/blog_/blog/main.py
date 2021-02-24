# type: ignore
import fastapi
from typing import List, Dict
from pydantic.main import create_model
import datetime

from sqlalchemy.engine import create_engine
import blog
from .models import schemas
from .models import models
from .database import engine, SessionLocal
from fastapi import Depends, status, Response, HTTPException
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

app = fastapi.FastAPI()

models.Base.metadata.create_all(bind=engine)  


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def index():
    return "Welcome to the blog"


# create a blog
@app.post('/blog', name='add_blog', status_code=status.HTTP_201_CREATED)
async def create(blog: schemas.Blog, db: Session = Depends(get_db)) -> models.Blog:
    now = datetime.datetime.now()
    new_blog = models.Blog(title=blog.title, 
                            body=blog.body, 
                            published=blog.published, 
                            created_at=now,)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# delete a blog
@app.delete('/blog/{id}', name="delete_blog", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog {id} not found in db, thus cannot deleted")
    
    blog.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/blog/{id}',  name="update_blog", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
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


# get all blogs in db
@app.get('/blog', name='all_blogs')
async def blogs_all(db: Session = Depends(get_db)) -> List:
    blogs = db.query(models.Blog).all()
    return blogs


# get a blog with blog id
@app.get('/blog/{id}', name='show_blog', status_code=200)
async def show_blog(id: int, response: Response, db: Session = Depends(get_db)) -> Dict:
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        data = {'detail': f"Blog {id} not found"}
        # return data
        #return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=data)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=data)
    return blog

