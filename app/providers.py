from collections.abc import Generator

from .services.scraper.scraper import ScraperService

scraper_service = ScraperService()


def provide_scraper_service() -> Generator:
    yield scraper_service
