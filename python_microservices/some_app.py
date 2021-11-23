import fastapi
from fastapi import status, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn

app = fastapi.FastAPI()

class Country_base(BaseModel):
    name: str
    capital: str
    area: int

class Country(Country_base):
    id: int

countries =[Country(id=1, name="Ghana", capital="Accra", area=585858585),
            Country(id=2, name="Nigeria", capital="Lagos", area=585858585),
            Country(id=3, name="UK", capital="London", area=585858585)]


@app.get("/countries",response_model=List[Country], status_code=status.HTTP_200_OK)
async def get_countries():
    return countries


@app.post("/countries", status_code= status.HTTP_201_CREATED)
async def add_country(country: Country_base):
    new_id = 3
    country_ = Country(id=new_id+1, name=country.name, capital=country.capital, area=country.area)
    countries.append(country_)
    new_id += 1
    return country_


@app.get("/countries/{id}")
async def get_country_by_id(id: int):
    country_len = len(countries)
    if id >= country_len:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Country id does not exist")
    return countries[id]



if __name__ == "__main__":
    uvicorn.run(app, port=8005, host='127.0.0.1')