import re

from src.features.systems.base import SystemTemplate
from src.utils.headers import build_general_header
from src.utils.strings import sanitize_attribute


class MagazineLuiza(SystemTemplate):
    system = "magazineluiza"
    base_url = "https://www.magazineluiza.com.br/"

    def __init__(self, product_url):
        super().__init__(product_url, force_visit_page=True)
        self.headers = build_general_header(
            authority="www.magazineluiza.com.br", random=True
        )

    @property
    def product_name(self) -> str:
        if name := self._last_response.html.xpath(
            "//h1[@class='header-product__title']", first=True
        ):
            return name.text
        return ""

    @property
    def sku(self) -> str:
        if sku_element := self._last_response.html.xpath(
            "//*[@class='header-product__code']", first=True
        ):
            sku_pattern = r"Código\s([a-z\d]+)\s"
            if match := re.search(sku_pattern, sku_element.text):
                return match.group(1)
        return ""

    @property
    def voltage(self) -> str:
        if volt_element := self._last_response.html.xpath(
            "//td[contains(text(), 'Voltagem')]/following-sibling::td", first=True
        ):
            return sanitize_attribute(volt_element.text)
        return ""

    @property
    def model(self):
        if model_element := self._last_response.html.xpath(
            "//td[contains(text(), 'Modelo')]/following-sibling::td", first=True
        ):
            return model_element.text
        return ""

    @property
    def color(self):
        # TODO GET color on site
        return ""

    @property
    def description(self) -> str:
        if description_element := self._last_response.html.xpath(
            "//div[@class='description__container-text']", first=True
        ):
            return description_element.text
        return ""

    @property
    def brand(self) -> str:
        if brand_element := self._last_response.html.xpath(
            "//a[@class='header-product__text-interation']/span", first=True,
        ):
            return brand_element.text
        return ""

    @property
    def image(self) -> str:
        if image_element := self._last_response.html.xpath(
            "//img[contains(@class, 'showcase-product__big-img')]", first=True,
        ):
            return image_element.attrs.get("src")
        return ""

    @property
    def url(self) -> str:
        return self._last_response.request.url.split("?")[0]

    @property
    def seller_name(self) -> str:
        if seller_element := self._last_response.html.xpath(
            "//button[contains(@class, 'seller-info-button')]", first=True,
        ):
            return seller_element.text
        elif self._last_response.html.xpath(
            (
                "//div[@class='seller__indentifier']"
                "/span[starts-with(@class, 'seller__indentifier-magazine')]"
            ),
            first=True,
        ):
            return "Magalu"
        return ""
