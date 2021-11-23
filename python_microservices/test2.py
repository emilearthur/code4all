import fastapi
import uvicorn

app = fastapi.FastAPI()

@app.get("/")
async def hello():
    return "Hello"

if __name__ == "__main__":
    uvicorn.run(app, port=8005, host='127.0.0.1')