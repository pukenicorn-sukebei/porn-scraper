from dataclasses import dataclass
from typing import Callable

xpath_type = Callable[[str, any], any] | str
optional_xpath_type = xpath_type | None


@dataclass
class ContentResultXPath:
    name: xpath_type
    code: xpath_type
    description: optional_xpath_type
    actors: xpath_type
    directors: optional_xpath_type
    tags: optional_xpath_type
    sample_video_urls: optional_xpath_type
    sample_image_urls: optional_xpath_type
    release_date: optional_xpath_type
    length: optional_xpath_type
    score: optional_xpath_type
    label: optional_xpath_type
    maker: optional_xpath_type
    cover_url: optional_xpath_type
