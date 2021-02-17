import fastapi
# import uvicorn
# import asyncio
# import json


app = fastapi.FastAPI()


@app.get('/', include_in_schema=False)
def index():
    return {'data': {'name': 'emile'}}


@app.get('/about')
def about():
    return {'data': 'about page'}

# if __name__ == "__main__":
#     uvicorn.run(app, port=8080, host='127.0.0.1')
# run app using 'uvicorn main:app --reload'
