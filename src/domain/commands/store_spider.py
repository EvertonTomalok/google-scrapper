import logging

from src.domain.pipelines.spider_run import build_spider_pipeline

logger = logging.getLogger(__name__)


def execute_spider(data: dict) -> dict:
    SPIDER_PIPELINE = build_spider_pipeline()
    try:
        result = SPIDER_PIPELINE.handle(data)
        return result
    except Exception as err:
        logger.error(err)
        return {}
