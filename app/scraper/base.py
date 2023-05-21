import logging
from datetime import datetime
from difflib import get_close_matches
from urllib.parse import urljoin
from lxml import html as l_html

from .client import SCRAPER
from .models import ContentResultXPath, ScrapedResult


class BaseScraper:
    _base_url: str
    _cookies: dict
    _headers: dict
    _date_format: str
    _allow_redirect: bool
    _search_exact_match: bool
    _encoding: str

    _search_result_xpath: str
    _content_result_xpath: ContentResultXPath

    def __init__(
            self,
            base_url: str,
            date_format: str,
            search_result_xpath: str,
            content_result_xpath: ContentResultXPath,
            cookies: dict = None,
            headers: dict = None,
            encoding='utf-8',
            allow_redirect=False,
            search_exact_match=False,
            logger_name=__name__
    ):
        self._base_url = base_url
        self._cookies = cookies if headers is not None else dict()
        self._headers = headers if cookies is not None else dict()
        self._date_format = date_format
        self._allow_redirect = allow_redirect
        self._search_exact_match = search_exact_match
        self._encoding = encoding
        self._search_result_xpath = search_result_xpath
        self._content_result_xpath = content_result_xpath

        self._logger = logging.getLogger(logger_name)

    def _get_search_path(self, query: str) -> str:
        raise NotImplementedError()

    def _get_video_path(self, query: str) -> str | None:
        raise NotImplementedError()

    ########################################################################

    def search(self, query: str, *, code: str = None, ) -> list[str]:
        path = self._get_search_path(query)
        self._logger.debug(f"Path: {path}")

        if self._search_exact_match:
            return self._execute_search(path)
        else:
            return get_close_matches(code or query, self._execute_search(path), cutoff=0)

    def fetch(self, video_path: str) -> ScrapedResult | None:
        if not video_path.startswith("http"):
            video_path = self._get_video_path(video_path)
            if video_path is None:
                return None

        return self._execute_fetch(video_path)

    ########################################################################

    def _execute_search(self, path: str) -> list[str]:
        url = self._base_url + path
        self._logger.debug(f"URL: {url}")
        with SCRAPER.get(url,
                         allow_redirects=self._allow_redirect,
                         cookies=self._cookies,
                         headers=self._headers) as res:
            # Check for errors
            try:
                res.raise_for_status()
            except:
                self._logger.debug(f"Failed to make request, {res.status_code}")
                return []

            if self._allow_redirect:
                self._logger.debug(f"Redirected URL: {res.url}")

            # Check for redirects
            redirect_location = res.headers.get("Location")
            if redirect_location and not self._allow_redirect:
                # Return redirect url if any
                self._logger.debug(f"Redirecting to {redirect_location}")
                return [urljoin(res.url, redirect_location)]

            tree = l_html.fromstring(res.content.decode(self._encoding, errors="ignore"))

        items = tree.xpath(self._search_result_xpath)
        self._logger.debug(f"Items: {items}")

        out = [urljoin(res.url, item.get("href")) for item in items]
        self._logger.debug(f"Out: {out}")

        return out

    def _execute_fetch(self, url: str) -> ScrapedResult | None:
        self._logger.debug(f"URL: {url}")
        with SCRAPER.get(
                url,
                cookies=self._cookies,
                headers=self._headers
        ) as res:
            # Check for errors
            try:
                res.raise_for_status()
                # callback = self.fail_callback
                # if callable(callback):
                #     callback(res)
            except:
                return None

            # Parse data
            tree = l_html.fromstring(res.content.decode(self._encoding))

        def handle_xpath(xpath, result_type=None):
            if xpath is None:
                if result_type is list:
                    return []
                else:
                    return None

            if callable(xpath):
                return xpath(res.url, tree)

            found = tree.xpath(xpath)

            self._logger.debug(f"found: '{result_type}', {found}")

            if result_type is list:
                return [x.text_content().strip() for x in found] if found else []
            elif result_type is datetime:
                return datetime.strptime(found[0].text_content().strip(), self._date_format) if found else None
            else:
                return found[0].text_content().strip() if found else None

        return ScrapedResult(
            code=handle_xpath(self._content_result_xpath.code),
            actors=handle_xpath(self._content_result_xpath.actors, list),
            name=handle_xpath(self._content_result_xpath.name),
            description=handle_xpath(self._content_result_xpath.description),
            tags=handle_xpath(self._content_result_xpath.tags, list),
            release_date=handle_xpath(self._content_result_xpath.release_date, datetime),
            length=handle_xpath(self._content_result_xpath.length),
            score=handle_xpath(self._content_result_xpath.score),
            label=handle_xpath(self._content_result_xpath.label),
            maker=handle_xpath(self._content_result_xpath.maker),
            cover_url=handle_xpath(self._content_result_xpath.cover_url),
            sample_video_urls=handle_xpath(self._content_result_xpath.sample_video_urls, list),
            sample_image_urls=handle_xpath(self._content_result_xpath.sample_image_urls, list),
        )
