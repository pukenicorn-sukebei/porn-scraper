import cloudscraper

__all__ = ['SCRAPER']

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/85.0.4183.121 Safari/537.36"

SCRAPER = cloudscraper.create_scraper(
    # Make sure mobile pages are not served
    browser={"custom": USER_AGENT}
)
