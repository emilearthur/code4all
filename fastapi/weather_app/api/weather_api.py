# type: ignore
from typing import Optional, List

import fastapi
from fastapi import Depends

from models.location import Location
from models.validation_error import ValidationError
from services import openweather_service
from services import report_service
from models.reports import Report, Report_submission


router = fastapi.APIRouter()


# coverting def weather to async

"""
@router.get('/api/weather/{city}')
def weather(city: str,
            country: Optional[str] = 'US',
            state: Optional[str] = None,
            units: str = 'metric'):

    report = await openweather_service.get_report(city, country, state, units)
    return report
"""


@router.get('/api/weather/{city}')
async def weather(loc: Location = Depends(), units: Optional[str] = 'metric'):
    try:
        return await openweather_service.get_report_async(loc.city, loc.state,
                                                          loc.country, units)
    except ValidationError as ve:
        return fastapi.Response(content=ve.error_msg, status_code=ve.status_code)

    except Exception as x:
        print(f"Server crashed while processing request: {x}")
        return fastapi.Response(content=str(x), status_code=500)


@router.get('/api/reports', name='all_reports', response_model=List[Report])
async def reports_get() -> List[Report]:
    # test
    # await report_service.add_report("A", Location(city="portland"))
    # await report_service.add_report("B", Location(city="new york"))
    return await report_service.get_reports()


@router.post('/api/reports', name='add_report', status_code=201, response_model=Report)
async def reports_post(report_submission: Report_submission) -> Report:
    description, location = report_submission.description, report_submission.location
    return await report_service.add_report(description, location)
