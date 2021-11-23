# type: ignore
import fastapi

from .models import models
from .database import engine

from .routers import blog
from .routers import user
from .routers import authenication


def configure_routing():
    app.include_router(authenication.router)
    app.include_router(blog.router)
    app.include_router(user.router)
    

app = fastapi.FastAPI()

models.Base.metadata.create_all(bind=engine)  

configure_routing()


@app.get('/')
def index():
    return "Welcome to the blog. Go to 127.0.0.1:8000/docs for more information about the API"
