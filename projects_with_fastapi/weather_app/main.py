# type: ignore
import fastapi
import uvicorn
import json
from fastcore.utils import Path
import asyncio

from starlette.staticfiles import StaticFiles

from api import weather_api
from views import home
from services import openweather_service
from models.location import Location
from services import report_service

api = fastapi.FastAPI()
# api = fastapi.FastAPI(docs_url=None) # uncomment to include docs


def configure():
    configure_routing()
    configure_apikeys()
    configure_fake_data()


def configure_apikeys():
    file = Path("settings.json")
    if not file.exists():
        print(f"WARNING: {file} not found, you cannot continue, please see \
            settings_template.json")
        raise Exception("setting.json file not found, you cannot continue, \
            please see setting_template")

    with open('settings.json') as fin:
        settings = json.load(fin)
        openweather_service.api_key = settings.get('api_key')


def configure_routing():
    api.mount('/static', StaticFiles(directory='static'), name='static')
    api.include_router(home.router)
    api.include_router(weather_api.router)


def configure_fake_data():
    "Added to test app"
    loc = Location(city="Accra")
    loc2 = Location(city="Portland", state="OR", country="US")
    asyncio.run(report_service.add_report("Heavy Rainfall", loc))
    asyncio.run(report_service.add_report("Clouds over downtown.", loc2))


if __name__ == "__main__":
    configure()
    uvicorn.run(api, port=8000, host='127.0.0.1')
else:
    configure()

# run uvicorn main :api
