from typing import List
from datetime import date

from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def get_all_todos() -> List[dict]:
    cleanings = [
        {"id": 1, "title": "Check data drift", "summary": "this is a sample test",
         "priority": "High", "DueDate": date.today()},
        {"id": 2, "title": "Documentation on me product", "summary": "ssome main to consider",
         "priority": "High", "DueDate": date.today()}
    ]
    return cleanings
