import javscraper

from app.scrapers.regex import guesser_regex, normalize_code


def guess(code: str) -> (any, str):
    # if guesser_regex['carib'].match(code):
    #     return javscraper.Caribbeancom, code
    if guesser_regex['heyzo'].match(code):
        return javscraper.Heyzo, code
    if guesser_regex['1pondo'].match(code):
        return javscraper.OnePondo, normalize_code(javscraper.OnePondo, code)
    # if regex_sod.match(code):
    #     return javscraper.sod

    return None, None
