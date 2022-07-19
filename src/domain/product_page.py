from logging import INFO, getLogger

from requests_html import HTMLSession

from src.domain.base import Base
from src.utils.strings import normalize_text

logger = getLogger()
logger.setLevel(INFO)


class GoogleProductPage(Base):
    def __init__(
        self,
        google_product_link: str,
        session: HTMLSession = None,
        headers: dict = None,
    ):
        super().__init__(session, headers)
        self.google_product_link = google_product_link

    def run(self):
        response = self._perform_request(
            self.google_product_link, method="get", headers=self.headers,
        )

        if not response or not response.ok:
            logger.critical(
                f"Stopping in first request url {self.google_product_link}..."
            )
            return None

        info_dict = {
            "all_stores_links": self._extract_comparing_all_stores_link(response),
            "name": normalize_text(self._extract_product_name(response)),
            "img": self._extract_product_img(response),
            "description": normalize_text(self._extract_description(response)),
        }

        if spec_element := response.html.xpath(
            "//a[text()='Ver todas as especificações']", first=True,
        ):
            nested_url = "https://www.google.com" + spec_element.attrs.get("href", "")
            response_page_spec = self._perform_request(
                nested_url, method="get", headers=self.headers,
            )

            if not response_page_spec or not response_page_spec.ok:
                logger.critical(f"Stopping in nested url {nested_url}...")
                return None

            info_dict.update(
                {
                    "brand": self._extract_brand(response_page_spec),
                    "skus": self._extract_skus(response_page_spec),
                    "ean": self._extract_ean(response_page_spec),
                }
            )
            return info_dict

        info_dict.update(
            {
                "brand": self._extract_brand(response),
                "skus": self._extract_skus(response),
                "ean": self._extract_ean(response),
            }
        )
        return info_dict

    @staticmethod
    def _extract_comparing_all_stores_link(response):
        if all_stores_element := response.html.xpath(
            "//a[@class='internal-link'][contains(text(),'Comparar preços de')]",
            first=True,
        ):
            if href := all_stores_element.attrs.get("href"):
                google_url = "https://www.google.com"
                return google_url + href if google_url not in href else href
        return ""

    @staticmethod
    def _extract_product_name(response):
        if name_element := response.html.xpath(
            "//span[contains(@class, 'sh-t__title-pdp')]", first=True
        ):
            return name_element.text
        return ""

    @staticmethod
    def _extract_product_img(response):
        if img_element := response.html.xpath(
            "//img[@class='sh-div__image sh-div__current']", first=True
        ):
            return img_element.attrs.get("src") or ""
        return ""

    @staticmethod
    def _extract_description(response):
        description = [
            f"- {span.text}"
            for span in response.html.xpath(
                "//div[@id='sg-product__pdp-container']//li/span"
            )
        ]

        return "\n".join(description) if description else ""

    @staticmethod
    def _extract_brand(response):
        if brand_element := response.html.xpath(
            "//td[contains(text(), 'Marca')]/following-sibling::td", first=True
        ):
            return normalize_text(brand_element.text)
        elif brand_element_variation := response.html.xpath(
            "//div[text()='Marca']/../following-sibling::td", first=True
        ):
            return normalize_text(brand_element_variation.text)
        return ""

    @staticmethod
    def _extract_skus(response):
        if skus_element := response.html.xpath(
            "//td[text()='Números da peça']/following-sibling::td", first=True
        ):
            return skus_element.text.split(", ")
        elif skus_element_variation := response.html.xpath(
            "//div[text()='Números da peça']/../following-sibling::td", first=True
        ):
            return skus_element_variation.text.split(", ")
        return []

    @staticmethod
    def _extract_ean(response):
        if ean_element := response.html.xpath(
            "//td[text()='GTIN']/following-sibling::td", first=True
        ):
            return ean_element.text.lstrip("0")
        elif ean_element_variation := response.html.xpath(
            "//div[text()='GTIN']/../following-sibling::td", first=True
        ):
            return ean_element_variation.text.lstrip("0")
        return ""
