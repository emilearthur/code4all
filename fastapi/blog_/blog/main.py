# type: ignore
import fastapi
from typing import List
import blog
from .models import schemas
from .models import models
from .database import engine, SessionLocal
from fastapi import Depends

from sqlalchemy.orm import Session

app = fastapi.FastAPI()

models.Base.metadata.create_all(bind=engine)  


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog')
def create(blog: schemas.Blog, db: Session = Depends(get_db)) -> models.Blog:
    new_blog = models.Blog(title=blog.title, 
                            body=blog.body, 
                            published=blog.published, 
                            created_at=blog.created_at,)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog')
def blogs_all(db: Session = Depends(get_db)) -> List:
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}')
def show_blog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    return blog

