from fastapi import FastAPI

from app.api import ping, notes
from app.database import engine, metadata, database

metadata.create_all(engine)

app = FastAPI(title="Notes")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(ping.router)
app.include_router(notes.router, prefix="/notes", tags=["notes"])
