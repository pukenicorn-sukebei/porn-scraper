from javscraper.utils import JAVResult

from ...scraper.models import ScrapedResult


def scraped_result_from_jav_result(jav_result: JAVResult) -> ScrapedResult:
    return ScrapedResult(
        code=jav_result.code,
        name=jav_result.name,
        description=jav_result.description,
        actors=jav_result.actresses,
        tags=jav_result.genres,
        sample_video_urls=[jav_result.sample_video] if jav_result.sample_video is not None else [],
        sample_image_urls=[],
        release_date=jav_result.release_date,
        score=jav_result.score,
        maker=jav_result.studio,
        cover_url=jav_result.image,
    )
