from dataclasses import dataclass
from datetime import datetime

from javscraper.utils import JAVResult


@dataclass
class ScrapedResult:
    code: str
    actors: list[str]
    tags: list[str]
    sample_video_urls: list[str]
    sample_image_urls: list[str]
    name: str | None = None
    description: str | None = None
    release_date: datetime | None = None
    length: int | None = None
    score: int | float = 0
    label: str | None = None
    maker: str | None = None
    cover_url: str | None = None
