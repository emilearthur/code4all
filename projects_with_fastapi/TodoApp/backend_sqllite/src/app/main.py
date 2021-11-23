import fastapi

from app.models import models
from app.database import engine

from app.routes import todo
from app.routes import user
from app.routes import authentication


def configure_routing():
    app.include_router(authentication.router, tags=['Authentication'])
    app.include_router(todo.router, prefix="/todos", tags=['TODO'])
    app.include_router(user.router, prefix="/user", tags=['Users'])


app = fastapi.FastAPI(title="TodoApp")

models.Base.metadata.create_all(bind=engine)
configure_routing()


@app.get('/')
def index():
    return "Welcome to the todo. Go to 127.0.0.1:8000/docs for more information about the API"
