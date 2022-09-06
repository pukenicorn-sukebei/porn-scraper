import javscraper

from app.scrapers.customs import JAVLibrary

default_scrapers = [
    JAVLibrary,
    # javscraper.Caribbeancom, # only works with title
    javscraper.OnePondo,
    javscraper.TenMusume,
    # javscraper.DMM, # jp result only
]

scrapers = dict()

scrapers[javscraper.JAVLibrary.__name__] = JAVLibrary('en')
# scrapers[javscraper.Caribbeancom.__name__] = javscraper.Caribbeancom('en') # only works with title
scrapers[javscraper.OnePondo.__name__] = javscraper.OnePondo(True)
scrapers[javscraper.TenMusume.__name__] = javscraper.TenMusume(True)
scrapers[javscraper.Heyzo.__name__] = javscraper.Heyzo(True)


def get(scraper):
    name = scraper.__name__
    if name not in scrapers:
        scrapers[name] = scraper()
    return scrapers[name]
