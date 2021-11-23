from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional


class CoreModel(BaseModel):
    """
    Any common logic shared by all model here
    """
    pass


class IDModelMixin(BaseModel):
    id: int


class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @validator("created_at", "updated_at", pre=True)  # validator sets default datetime fot both created_at and updated_at fields
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.datetime.now()
