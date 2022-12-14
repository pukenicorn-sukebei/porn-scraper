import logging

from fastapi import APIRouter, HTTPException
from javscraper.utils import JAVResult

from app import scrapers
from app.scrapers.scrape import scrape

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/{code}",
    response_model=JAVResult,
)
async def lookup(code: str):
    guessed_scraper, suggested_code = scrapers.guess(code)
    if guessed_scraper is not None:
        scraper = scrapers.get(guessed_scraper)
        logger.info("Getting from guessed: {}".format(guessed_scraper.__name__))
        result = scrape(scraper, suggested_code)

        if result is not None:
            logger.info("Found guessed: {}".format(guessed_scraper.__name__))
            return result
        logger.info("Not found guessed: {}".format(guessed_scraper.__name__))

    for default_scraper in scrapers.default_scrapers:
        if default_scraper == guessed_scraper:
            pass

        scraper = scrapers.get(default_scraper)
        logger.info("Getting from list: {}".format(default_scraper.__name__))
        result = scrape(scraper, code)

        if result is not None:
            logger.info("Found list: {}".format(default_scraper.__name__))
            return result
        logger.info("Not found list: {}".format(default_scraper.__name__))

    raise HTTPException(status_code=404)

