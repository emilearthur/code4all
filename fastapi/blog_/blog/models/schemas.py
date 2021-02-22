# type: ignore
from typing import Optional
import datetime
from pydantic import BaseModel

class Blog_submission(BaseModel):
    title: str
    body: str
    published: Optional[bool]


class Blog(Blog_submission):
    created_at: Optional[datetime.datetime]
