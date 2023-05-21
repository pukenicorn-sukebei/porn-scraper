import logging

from fastapi import APIRouter, HTTPException, Depends

from app import providers
from app.scraper.models import ScrapedResult
from app.services.scraper.scraper import ScraperService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/{code}",
    response_model=ScrapedResult,
)
async def lookup(
        code: str,
        scraper_service: ScraperService = Depends(providers.provide_scraper_service),
):
    result = scraper_service.guess_scape(code)

    if result is None:
        raise HTTPException(status_code=404)

    return result
