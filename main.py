from fastapi import FastAPI
from pydantic import BaseModel
import financedatabase as fd

app = FastAPI()
equities = fd.Equities()


@app.get("/equities/countries")
async def get_equities_countries():
    """
    Endpoint to obtain all countries from the Equities database.
    """
    equities_countries = equities.options('country')
    return {"countries": list(equities_countries)}


@app.get("/equities/sectors")
async def get_equities_sectors():
    """
    Endpoint to obtain all sectors from the Equities database.
    """
    equities_sectors = equities.options('sector')
    return {"sectors": list(equities_sectors)}


@app.get("/equities/industry_groups")
async def get_equities_industry_groups():
    """
    Endpoint to obtain all industry groups from the Equities database.
    """
    equities_industry_groups = equities.options('industry_group')
    return {"industry_groups": list(equities_industry_groups)}


@app.get("/equities/industries/{country}")
async def get_equities_industries(country: str):
    """
    Endpoint to obtain all industries from a country from the Equities database.
    """
    equities_industries = equities.options('industry', country=country)
    return {"industries": list(equities_industries)}


class SearchRequest(BaseModel):
    country: str = None
    industry: str = None
    exchange: str = None


@app.post("/equities/search")
async def search_equities(search_request: SearchRequest):
    """
    Endpoint to search specific fields in the Equities database, based on user input.
    """
    search_params = {}
    if search_request.country:
        search_params['country'] = search_request.country
    if search_request.industry:
        search_params['industry'] = search_request.industry
    if search_request.exchange:
        search_params['exchange'] = search_request.exchange

    search_results = equities.search(**search_params)
    return {"equities": search_results}
