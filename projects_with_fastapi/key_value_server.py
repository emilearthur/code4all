"""Server with fastapi that generates key-value pair of random generated UUDI and timestamp.

Key is time stamp, value is UUID.
Output of API call is
{

"2021-05-21 12:10:19.484523": "e8c928fea580474cae5aa3934c59c26f"

"2021-05-21 12:08:25.751933": "fcd25b46bec84ef79e14410b91fbf0b3",

"2021-05-21 12:07:27.150522": "6270d1d412b546a28b7d2c98130e1a5a",

}
"""

import fastapi
import uvicorn
from datetime import datetime
from pydantic import BaseModel
import uuid
from typing import Dict
from collections import OrderedDict


class KeyValue(BaseModel):
    """Class for data output."""

    date: datetime
    UUID: str


_saved_keys_: Dict[str, str] = {}

app = fastapi.FastAPI()


@app.get("/get_generate_keys/")
async def root():
    """Get datetime and UUID when endpoint is called."""
    key_value = KeyValue(date=datetime.now(), UUID=uuid.uuid4().hex)
    _saved_keys_[key_value.date] = key_value.UUID

    return OrderedDict(sorted(_saved_keys_.items(), reverse=True))


if __name__ == "__main__":
    uvicorn.run(app, port=8005, host='127.0.0.1')
