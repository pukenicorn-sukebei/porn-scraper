import re
from urllib.parse import quote

from ..base import BaseScraper
from ..models import ContentResultXPath


class JavLibraryScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            logger_name=__name__,
            base_url='https://www.javlibrary.com',
            cookies={"over18": "18"},
            date_format='%Y-%m-%d',
            search_exact_match=True,
            search_result_xpath="/html/body/div[3]/div[2]/div[2]/div/div[@class='video']/a",
            content_result_xpath=ContentResultXPath(
                code="//div[@id='video_id']/table/tr/td[2]",
                name=self._get_name_xpath,
                description=None,
                length="//div[@id='video_length']/table/tr/td[2]/span",
                maker="//div[@id='video_maker']/table/tr/td[2]/span/a",
                label="//div[@id='video_label']/table/tr/td[2]/span/a",
                cover_url=self._get_cover_url_xpath,
                sample_video_urls=None,
                sample_image_urls=self._get_sample_image_urls_xpath,
                actors="//span[@class='star']/a",
                directors="//div[@id='video_director']/table/tr/td[2]/span/a",
                tags="//span[@class='genre']/a",
                release_date="//div[@id='video_date']/table/tr/td[2]",
                score=self._get_score_xpath
            ),
        )
        self.locale = 'en'

    def _get_search_path(self, query: str) -> str:
        return f"/{self.locale}/vl_searchbyid.php?keyword={quote(query)}"

    def _get_video_path(self, query: str) -> str | None:
        video_url = self.search(query)
        if len(video_url) == 0:
            return None

        self._logger.debug(f"Found video {video_url[0]}")
        return video_url[0]

    @staticmethod
    def _get_name_xpath(url: str, tree) -> str:
        value = tree.xpath("//h3[contains(@class, 'post-title')]")[0].text_content()
        code = tree.xpath("//div[@id='video_id']/table/tr/td[2]")[0].text_content()
        return value.replace(code, "").strip()

    @staticmethod
    def _get_cover_url_xpath(url: str, tree) -> str:
        value = tree.xpath("//img[@id='video_jacket_img']")[0]
        return value.get("src")

    @staticmethod
    def _get_sample_image_urls_xpath(url: str, tree) -> list[str]:
        values = tree.xpath("//div[@class='previewthumbs']/img")
        return [value.get("src") for value in values]

    @staticmethod
    def _get_score_xpath(url: str, tree) -> float:
        value = tree.xpath("//div[@id='video_review']//span/text()")
        if not value:
            return 0.0

        return float(re.search(r"\(([0-9.]+)\)", "".join(value)).group(1))
