from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
import uvicorn
from pydantic import BaseModel

_USERS = {'1': 'Tarek', '2': 'Freya'}
_IDS = {val: id for id, val in _USERS.items()}

app = FastAPI()


@app.get("/api",name="api", response_model=str, status_code=status.HTTP_200_OK)
async def my_microservice():
    response = JSONResponse(content={"Hello": "World!"})
    return response


@app.get("/api/person/{person_id}", response_model=str)
async def person(person_id:int):
    if str(person_id) not in _USERS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    name = _USERS[str(person_id)]
    response = JSONResponse(content={"Hello hey": name})
    return response


if __name__ == "__main__":
    uvicorn.run(app, port=8005, host='127.0.0.1')