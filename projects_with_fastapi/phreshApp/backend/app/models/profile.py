from typing import Optional
from pydantic import EmailStr, HttpUrl

from app.models.core import DateTimeModelMixin, IDModelMixin, CoreModel


class ProfileBase(CoreModel):
    full_name: Optional[str]
    phone_number: Optional[str]
    bio: Optional[str]
    image: Optional[HttpUrl]


class ProfileCreate(ProfileBase):
    """ Field required to create profile """
    user_id: int


class ProfileUpdate(ProfileBase):
    """ Allows user to update profile. user_id cannot be updated """
    pass


class ProfileInDB(IDModelMixin, DateTimeModelMixin, ProfileBase):
    user_id: int
    username: Optional[str]
    email: Optional[EmailStr]


class ProfilePublic(ProfileInDB):
    pass
