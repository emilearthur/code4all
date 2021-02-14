# type: ignore
from typing import Optional, Tuple
from models.validation_error import ValidationError
import requests
import httpx

from infastructure import weather_cache

api_key: Optional[str] = None


def get_report(city: str, state: Optional[str], country: str,
               units: str) -> dict:
    if state:
        q = f'{city},{state},{country}'
    else:
        q = f'{city},{country}'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={q}&appid={api_key}&units={units}'
    resp = requests.get(url, verify=False)
    resp.raise_for_status()

    data = resp.json()
    forecast = data['main']
    return forecast


async def get_report_async(city: str, state: Optional[str], country: str,
                           units: str) -> dict:
    city, state, country, units = validate_units(city, state, country, units)

    forecast = weather_cache.get_weather(city, state, country, units)
    if forecast:
        return forecast

    if state:
        q = f'{city},{state},{country}'
    else:
        q = f'{city},{country}'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={q}&appid={api_key}&units={units}'

    async with httpx.AsyncClient() as client:
        r: httpx.Response = await client.get(url)
        if r.status_code != 200:
            raise ValidationError(r.text, status_code=r.status_code)

    forecast = r.json()['main']

    weather_cache.set_weather(city, state, country, units, forecast)

    return forecast


def validate_units(city: str, state: Optional[str], country: Optional[str],
                   units: str) -> Tuple[str, str, str, str]:
    city = city.lower().strip()
    if not country:
        country = "us"
    else:
        country = country.lower().strip()

    if len(country) != 2:
        error = f"Invalid country: {country}. It must be a two letter abbrevation \
            such as US or GB or GH"
        raise ValidationError(status_code=400, error_msg=error)

    if state:
        state = state.strip().lower()

    if state and len(state) != 2:
        error = f"Invalid state: {state}. It must be a two letter abbreaviation \
            such as CA or KS "
        raise ValidationError(status_code=400, error_msg=error)

    if units:
        units = units.strip().lower()

    valid_units = {'standard', 'metric', 'imperial'}
    if units not in valid_units:
        error = f"Invalid units '{units}', it must be one of {valid_units}."
        raise ValidationError(status_code=400, error_msg=error)

    return city, state, country, units
