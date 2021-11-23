from pydantic import BaseModel, EmailStr, conint
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    lname: str
    fname: str
    password: str


class User(BaseModel):
    email: str
    id: int

    class Config():
        orm_mode = True


# create a TODO
class TODOCreate(BaseModel):
    text: str
    completed: bool
    priority: conint(ge=0, le=2)  # Priority 0-Higher, 1-High, 2 - Less Higher


# update an existing TODO
class TODOUpdate(TODOCreate):
    id: int


class TODO(TODOCreate):
    id: int

    class Config():
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
