
# modifying the previous function with good design in mind.

from collections import Counter
from fastapi import status, FastAPI, Response, Request
from abc import ABC, abstractmethod
from redis import Redis
from typing import Dict
import uvicorn


class ViewStorageBackend(ABC):
    @abstractmethod
    def increment(self, key: str) -> None:
        ...

    @abstractmethod
    def most_common(self, n: int) -> Dict[str, int]: 
        ...


class CounterBackend(ViewStorageBackend):
    """This implementation adapts Counter class into the ViewsStorageBackend
    Infterface.
    """
    def __init__(self):
        self._counter = Counter()

    def increment(self, key: str) -> None:
        self._counter[key] += 1

    def most_common(self, n: int) -> Dict[str, int]:
        return dict(self._counter.most_common(n))


class RedisBackend(ViewStorageBackend):
    """Storage using redis"""
    def __init__(self, redis_client: Redis, set_name: str) -> None:
        self._client = redis_client
        self._set_name = set_name

    def increment(self, key: str) -> None:
        self._client.zincrby(self._set_name, 1, key)

    def most_common(self, n: int) -> Dict[str, int]:
        return {key.decode(): int(value) for key, value 
                in self._client.zrange(self._set_name, 0, n-1,
                                       desc=True, withscores=True,)}

app = FastAPI(title="IoC Web Application")

storage = RedisBackend(Redis(host="redis"), "my-stats")

PIXEL = (
    b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00'
    b'\x00\x00\xff\xff\xff!\xf9\x04\x01\x00'
    b'\x00\x00\x00,\x00\x00\x00\x00\x01\x00'
    b'\x01\x00\x00\x02\x01D\x00;'
    )

@app.get("/track")
def track(request: Request, storage: ViewStorageBackend = storage):
    try:
        referer =  request.headers["Referer"]
    except KeyError:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    storage.increment(referer)
    
    return Response(content=PIXEL,
                    headers={
                        "Content-Type": "image/gif",
                        "Expires": "Mon, 01 Jan 1990 00:00:00 GMT",
                        "Cache-Control": "no-cache, no-store, must-revalidate",
                        "Pragma": "no-cache",
                    }
    )

@app.get("/stats")
def stats(storage: ViewStorageBackend = storage):
    return storage.most_common(10)

@app.get("/test")
def test(request: Request, storage: ViewStorageBackend = storage):
    return """
    <html>
    <head></head>
    <body><img src="/track"></body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run(app, port=8005, host='127.0.0.1')
