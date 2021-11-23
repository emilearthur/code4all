# type: ignore

from typing import Optional
import fastapi
from models.blog import Blog
# import uvicorn
# import asyncio
# import json


app = fastapi.FastAPI()


@app.get('/blog')
def index(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {'data': f'{limit} published blog from the db'}
    else:
        return {'data': f'{limit} blog from the db'}


@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blogs'}


@app.get('/blog/{id}')
def show(id: int):
    # fetch blog with id=id
    return {'data': id}


@app.get('/blog/{id}/comments')
def comments(id: int, limit: int = 10):
    # fetch comments of blog with id=id
    return {'data': {'1', '2'}}


@app.get('/about')
def about():
    return {'data': 'about page'}


@app.post('/blog')
def create_blog(blog: Blog):
    return {'data': f"Blog create with title {blog.title} at {blog.created_at}"}

# if __name__ == "__main__":
#    uvicorn.run(app, port=8080, host='127.0.0.1')
# run app using 'uvicorn main:app --reload'
