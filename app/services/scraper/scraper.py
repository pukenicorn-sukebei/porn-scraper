import logging

import javscraper
from javscraper.base import Base as JavScraperBase
from javscraper.utils import JAVResult

from .regex import guesser_regex, normalize_code
from .utils import scraped_result_from_jav_result
from ...scraper.base import BaseScraper
from ...scraper.models import ScrapedResult
from ...scraper.scrapers.javlibrary import JavLibraryScraper


class ScraperService:
    def __init__(self):
        self._logger = logging.getLogger(__name__)

        self._default_scraper_order = [
            JavLibraryScraper,
            # javscraper.Caribbeancom, # only works with title
            javscraper.OnePondo,
            javscraper.TenMusume,
            # javscraper.DMM, # jp result only
        ]

        self._scrapers = {
            JavLibraryScraper: JavLibraryScraper(),
            javscraper.OnePondo: javscraper.OnePondo(True),
            javscraper.TenMusume: javscraper.TenMusume(True),
            javscraper.Heyzo: javscraper.Heyzo(True),
        }

    def guess_scape(self, code: str) -> ScrapedResult | None:
        guessed_scraper, suggested_code = self.guess(code)
        if guessed_scraper is not None:
            scraper = self._scrapers[guessed_scraper]
            self._logger.info("Getting from guessed: {}".format(guessed_scraper.__name__))
            result = self.scrape(scraper, suggested_code)

            if result is not None:
                self._logger.info("Found guessed: {}".format(guessed_scraper.__name__))
                return result
            self._logger.info("Not found guessed: {}".format(guessed_scraper.__name__))

        for default_scraper in self._default_scraper_order:
            if default_scraper == guessed_scraper:
                pass

            scraper = self._scrapers[default_scraper]
            self._logger.info("Getting from list: {}".format(default_scraper.__name__))
            result = self.scrape(scraper, code)

            if result is not None:
                self._logger.info("Found list: {}".format(default_scraper.__name__))
                return result
            self._logger.info("Not found list: {}".format(default_scraper.__name__))

    @staticmethod
    def guess(code: str) -> (JavScraperBase | BaseScraper, str):
        # if guesser_regex['carib'].match(code):
        #     return javscraper.Caribbeancom, code
        if guesser_regex['heyzo'].match(code):
            return javscraper.Heyzo, code
        if guesser_regex['1pondo'].match(code):
            return javscraper.OnePondo, normalize_code(javscraper.OnePondo, code)
        # if regex_sod.match(code):
        #     return javscraper.sod

        return None, None

    def scrape(self, scraper, code: str) -> ScrapedResult | None:
        def result_wrapper(res: JAVResult | ScrapedResult | None):
            if res is None:
                return None
            if res is JAVResult:
                return scraped_result_from_jav_result(res)
            return res

        normalized_code = normalize_code(type(scraper), code)
        result = (scraper.fetch if issubclass(scraper.__class__, BaseScraper) else scraper.get_video)(normalized_code)
        result = result_wrapper(result)

        if result is None:
            return None
        if self._validate_result(scraper, result, normalized_code):
            self._logger.info("Got {} from get".format(normalized_code))
            return result

        try:
            search_results = scraper.search(normalized_code)
            self._logger.info("Got list: {}, {} items".format(type(scraper).__name__, len(search_results)))
        except NotImplementedError:
            return

        for search_result in search_results:
            result = (scraper.fetch if issubclass(scraper.__class__, BaseScraper) else scraper.get_video)(search_result)
            result = result_wrapper(result)

            if self._validate_result(scraper, result, normalized_code):
                return result

    def _validate_result(self, scraper, result: ScrapedResult, normalized_code: str) -> bool:
        if result is None:
            return True

        normalized_result_code = normalize_code(type(scraper), result.code)
        matched = normalized_result_code == normalized_code
        if not matched:
            self._logger.info('Looking for {} but got {} instead'.format(normalized_code, normalized_result_code))
        return matched
