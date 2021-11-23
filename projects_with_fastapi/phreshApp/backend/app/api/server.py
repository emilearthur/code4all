from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.core import config, tasks


def get_application():
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get('/')
    def index():
        return f"Welcome to the {config.PROJECT_NAME}. Go to 127.0.0.1:8000/docs for more information about the API"

    app.add_event_handler("startup", tasks.create_start_app_handler(app))
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))

    app.include_router(api_router, prefix="/api")
    return app


app = get_application()
