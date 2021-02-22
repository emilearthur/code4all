# type: ignore
import fastapi
from typing import List, Dict
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


@app.post('/blog', name='add_blog', status_code=status.HTTP_201_CREATED)
async def create(blog: schemas.Blog, db: Session = Depends(get_db)) -> models.Blog:
    new_blog = models.Blog(title=blog.title, 
                            body=blog.body, 
                            published=blog.published, 
                            created_at=blog.created_at,)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete('/blog/{id}', name="delete_blog", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get('/blog', name='all_blogs')
async def blogs_all(db: Session = Depends(get_db)) -> List:
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', name='show_blog', status_code=200)
async def show_blog(id, response: Response, db: Session = Depends(get_db)) -> Dict:
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        data = {'detail': f"Blog {id} not found"}
        # return data
        #return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=data)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=data)
    return blog

