# type: ignore
from typing import Optional, List
import datetime
from pydantic import BaseModel


# Model for blog
class Blog_submission(BaseModel):
    title: str
    body: str
    published: Optional[bool] = False


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


# Model for User
class User(BaseModel):
    name: str
    email: str
    password: str


class User_extend(User):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    DOB: datetime.date
    disabled: Optional[bool] = None


# Model for login
class Login(BaseModel):
    username: str
    password: str


# response model for User
class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []
    class Config():
        orm_mode = True


# Response Model for Blog
class ShowBlog(Blog):
    creator: ShowUser
    class Config():
        orm_mode = True


# Model for token 
class Token(BaseModel):
    access_token: str
    token_type: str  


class TokenData(BaseModel):
    username: Optional[str] = None
