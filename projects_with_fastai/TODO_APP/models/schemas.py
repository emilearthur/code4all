from pydantic import BaseModel
from pydantic import EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    lname: str
    fname: str
    password: str


class User(BaseModel):
    fname: str
    email: str

    class Config():
        orm_mode = True


# create a TODO
class TODOCreate(BaseModel):
    text: str
    compeleted: bool
    priority: int


# update an existing TODO
class TODOUpdate(TODOCreate):
    id: int


class TODO(TODOCreate):
    class Config():
        orm_mode = True
