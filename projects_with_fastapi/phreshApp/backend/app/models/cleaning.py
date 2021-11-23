from typing import Optional, Union
from enum import Enum

from app.models.core import IDModelMixin, CoreModel, DateTimeModelMixin
from app.models.user import UserPublic


class CleaningType(str, Enum):  # this only takes 3 values
    dust_up = "dust_up"
    spot_clean = "spot_clean"
    full_clean = "full_clean"


class CleaningBase(CoreModel):
    """ All common x'tics of cleaning resources"""
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    cleaning_type: Optional[CleaningType] = "spot_clean"


class CleaningCreate(CleaningBase):
    """atttribute required to create a new resource - POST"""
    name: str
    price: float


class CleaningUpdate(CleaningBase):
    """atttribute required to update a new resource - PUT"""
    cleaning_type: Optional[CleaningType]


class CleaningInDB(IDModelMixin, DateTimeModelMixin, CleaningBase):
    """atttribute presented on any resouce from the db"""
    name: str
    price: float
    cleaning_type: CleaningType
    owner: int


class CleaningPublic(CleaningInDB):
    """atttribute presented on public facing resouces return GET, POST, PUT request"""
    owner: Union[int, UserPublic]
