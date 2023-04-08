
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import financedatabase as fd
from financedatabase.Equities import Equities
from typing import Optional, List, Dict

equities_app = FastAPI()

equities = fd.Equities()

class SearchRequest(BaseModel):
    country: str = None
    industry: str = None
    exchange: str = None


@equities_app.post("/search")
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


class EquitiesRequest(BaseModel):
    country: Optional[str] = ""
    sector: Optional[str] = ""
    industry_group: Optional[str] = ""
    industry: Optional[str] = ""
    exclude_exchanges: Optional[bool] = True
    capitalize: Optional[bool] = True

class EquityData(BaseModel):
    name: Dict[str, str]
    summary: Dict[str, str]
    currency: Dict[str, str]
    sector: Dict[str, str]
    industry_group: Dict[str, str]
    industry: Dict[str, str]
    exchange: Dict[str, str]
    market: Dict[str, str]
    country: Dict[str, str]
    state: Dict[str, Optional[str]]
    city: Dict[str, str]
    zipcode: Dict[str, str]
    website: Dict[str, str]
    market_cap: Dict[str, str]
    isin: Dict[str, Optional[str]]
    cusip: Dict[str, Optional[str]]
    figi: Dict[str, Optional[str]]
    composite_figi: Dict[str, Optional[str]]
    shareclass_figi: Dict[str, Optional[str]]

class EquitiesResponse(BaseModel):
    data: List[EquityData]


@equities_app.post("/", response_model = EquitiesResponse)
async def get_equities(request: EquitiesRequest):
    try:
        equities_df = Equities().select(
            country=request.country,
            sector=request.sector,
            industry_group=request.industry_group,
            industry=request.industry,
            exclude_exchanges=request.exclude_exchanges,
            capitalize=request.capitalize
        )
        return {"data": equities_df.head().to_json(orient="records")}
    except Exception as e:
        return JSONResponse(content={"error": str(e)})

class OptionsRequest(BaseModel):
    selection: str
    country: Optional[str] = ""
    sector: Optional[str] = ""
    industry_group: Optional[str] = ""
    industry: Optional[str] = ""

class OptionsResponse(BaseModel):
    data: List[str]

@equities_app.post("/options/", response_model=OptionsResponse)
async def get_options(request: OptionsRequest):
    try:
        options = Equities().options(
            selection=request.selection,
            country=request.country,
            sector=request.sector,
            industry_group=request.industry_group,
            industry=request.industry
        )
        return {"data": list(options)}
    except Exception as e:
        return JSONResponse(content={"error": str(e)})