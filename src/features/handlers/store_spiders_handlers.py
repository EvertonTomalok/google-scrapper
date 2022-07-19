import logging
from typing import List, Type

from src.features.handlers.base_handler import AbstractHandler
from src.features.systems.base import SystemTemplate
from src.helpers.saving import saving_on_data_quality, saving_product
from src.helpers.systems_loader import load_system_classes

logger = logging.getLogger(__name__)


class LoadSystem(AbstractHandler):
    def handle(self, request):
        if (
            isinstance(request, dict)
            and request.get("system")
            and request.get("product_link")
        ):
            system = request.get("system", "").lower()
        else:
            raise ValueError(
                "'system' and 'product_link' must be on a dict like "
                "{'system': 'magazineluiza', 'product_link': 'http://...'}"
            )

        system_loaded = load_system_classes(system)

        if system_loaded:
            request["system_classes"] = system_loaded
            return super().handle(request)
        return False


class RunSystem(AbstractHandler):
    def __init__(self):
        self.products_variation = []

    def handle(self, request: dict):
        if request.get("system_classes") and request.get("product_link"):
            try:
                system_classes: List[Type[SystemTemplate]] = request.get(
                    "system_classes"
                )

                spider_class = system_classes[0]

                # Crawling MAIN AD
                self._crawl(request, request.get("product_link"), spider_class)

                # Crawling all other ADS
                for ad in request.get("ads", []):
                    if ad_link := ad.get("ad_link"):
                        self._crawl(request, ad_link, spider_class)
                return super().handle(self.products_variation)
            except Exception as err:
                logger.critical(f"RunSystemError: {type(err)} -> {err}")
        return False

    def _crawl(self, request, link, spider_class):
        spider = spider_class(link)
        result = spider.run()

        if result:
            for product in result:
                self.products_variation.append({**request, **product})


class SaveProduct(AbstractHandler):
    def handle(self, request: List[dict]):
        for product in request:
            saving_product(product)
            saving_on_data_quality(product)

        if request:
            return super().handle(request)
        return False
