# type: ignore
import fastapi
from fastapi import Depends, status, Response, HTTPException
from fastapi.responses import JSONResponse

from typing import List, Dict
import datetime

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session

from .models import schemas
from .models import models
from .database import engine, SessionLocal
from .hashing import Hash



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
@app.post('/blog', name='create_blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
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
@app.delete('/blog/{id}', name="delete_blog", status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
async def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog {id} not found in db, thus cannot deleted")
    
    blog.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update blog
@app.put('/blog/{id}',  name="update_blog", status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
async def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
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
@app.get('/blog', name='all_blogs', response_model=List[schemas.ShowBlog], tags=['blogs'])
async def blogs_all(db: Session = Depends(get_db)) -> List:
    blogs = db.query(models.Blog).all()
    return blogs


# get a blog with blog id
@app.get('/blog/{id}', name='show_blog', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['blogs'])
async def show_blog(id: int, response: Response, db: Session = Depends(get_db)) -> Dict:
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        details = f"Blog {id} not found"
        # return data
        #return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=data)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=details)
    return blog





# creating a user 
@app.post('/user', name="create_user", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser, tags=['users'])
async def create_user(user: schemas.User, db: Session = Depends(get_db)) -> models.User:
    new_user = models.User(name = user.name,
                           email = user.email, 
                           password = Hash.bcryt(user.password))
    db.add(new_user) 
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user/{id}', name="get_user", response_model=schemas.ShowUser, tags=['users'])
def get_user(id: int,  db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        details = f"User not found"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=details)
    return user



