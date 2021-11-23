# type: ignore
from typing import Optional
from pydantic import BaseModel
from models.location import Location
import datetime


class Report_submission(BaseModel):
    description: str
    location: Location


class Report(Report_submission):
    id: str
    created_date: Optional[datetime.datetime]
