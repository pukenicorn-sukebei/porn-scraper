import logging

from javscraper.utils import JAVResult

from app.scrapers.customs import JAVLibrary
from app.scrapers.regex import normalize_code


logger = logging.getLogger(__name__)


def scrape(scraper, code: str):
    normalized_code = normalize_code(type(scraper), code)
    result = scraper.get_video(normalized_code)

    if _validate_result(scraper, result, normalized_code):
        logger.info("Got {} from get".format(normalized_code))
        return result

    try:
        if type(scraper) == JAVLibrary:
            search_results = scraper.search(normalized_code, code=normalized_code)
        else:
            search_results = scraper.search(normalized_code)
        logger.info("Got list: {}, {} items".format(type(scraper).__name__, len(search_results)))
    except NotImplementedError:
        return

    for search_result in search_results:
        result = scraper.get_video(search_result)

        if _validate_result(scraper, result, normalized_code):
            return result


def _validate_result(scraper, result: JAVResult, normalized_code: str) -> bool:
    """
    Returns:
        True if result is valid or None
        False if result exists but differs from code
    """
    if result is None:
        return True

    normalized_result_code = normalize_code(type(scraper), result.code)
    matched = normalized_result_code == normalized_code
    if not matched:
        logger.info('Looking for {} but got {} instead'.format(normalized_code, normalized_result_code))
    return matched
