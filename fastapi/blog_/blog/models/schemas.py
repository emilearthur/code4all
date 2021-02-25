# type: ignore
from typing import Optional, List
import datetime
from pydantic import BaseModel

class Blog_submission(BaseModel):
    title: str
    body: str
    published: Optional[bool]


class BlogBase(Blog_submission):
    created_at: Optional[datetime.datetime]


class Blog(BlogBase):
    class Config():
        orm_mode = True

# getting only the title as a response
# class ShowBlog(BaseModel):
#     title:str
#     class Config():
#         orm_mode = True

class User(BaseModel):
    name: str
    email: str
    password: str


class User_extend(User):
    first_name: str
    last_name: str
    middle_name: Optional[str]
    DOB: datetime.date


# response model 
class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []
    class Config():
        orm_mode = True


# response model 
class ShowBlog(Blog):
    creator: ShowUser
    class Config():
        orm_mode = True
