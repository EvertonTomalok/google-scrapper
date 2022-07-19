from dataclasses import dataclass
from datetime import datetime
from typing import Union

from dataclasses_json import dataclass_json
from requests_html import HTMLSession

from src.domain.base import Base
from src.features.get_systems import available_systems
from src.helpers.queue_consumers_and_producers import ProductsQueue
from src.utils.enumerators import EanSearchStatus

GOOGLE_URL = "https://www.google.com"


@dataclass_json
@dataclass
class EanResult:
    status: str
    product_link: str
    redirect_directly_to_store: bool


class GoogleSearchEAN(Base):
    def __init__(self, ean: str, session: HTMLSession = None, headers: dict = None):
        super().__init__(session, headers)
        self.ean = ean

    def run(self) -> Union[dict, bool]:
        response = self._perform_search(self.ean)
        if not response.ok:
            return {}

        ean_search_result = self._extract_price_comparing_link_object(response)

        if ean_search_result.status == EanSearchStatus.NOT_FOUND.value:
            return {"status": EanSearchStatus.NOT_FOUND.value}

        elif ean_search_result.status == EanSearchStatus.MULTIPLE_RESULTS.value:
            return {
                "search_ean": self.ean,
                "single_store": False,
                "status": EanSearchStatus.MULTIPLE_RESULTS.value,
                "product_link": ean_search_result.product_link,
            }

        elif ean_search_result.status == EanSearchStatus.UNIQUE_STORE.value:
            self._send_single_product_to_queue(response)
            return {
                "search_ean": self.ean,
                "single_store": True,
                "status": EanSearchStatus.UNIQUE_STORE.value,
                "product_link": ean_search_result.product_link,
            }

        return {
            "search_ean": self.ean,
            "product_link": ean_search_result.product_link,
            "status": EanSearchStatus.SUCCESS.value,
        }

    def _perform_search(self, ean: str):
        params = {
            "q": ean,
            "hl": "pt-BR",
            "source": "lnms",
            "tbm": "shop",
            "cr": "countryBR",
        }
        url = f"{GOOGLE_URL}/search"

        return self._perform_request(
            url, method="get", params=params, headers=self.headers,
        )

    def _extract_price_comparing_link_object(self, response) -> EanResult:
        if list_redirect_link_element := response.html.xpath(
            "//a[starts-with(text(),'Comparar preços')]"
        ):
            if len(list_redirect_link_element) > 1:
                """
                If we found more than one link to compare prices, we can't
                have 100% sure about it's the right link to this ean.
                So, skip it and save on database as multiple link to this ean.
                """
                return EanResult(
                    status=EanSearchStatus.MULTIPLE_RESULTS.value,
                    product_link="",
                    redirect_directly_to_store=False,
                )
            elif link := list_redirect_link_element[0].attrs.get("href"):
                link = GOOGLE_URL + link if GOOGLE_URL not in link else link
                return EanResult(
                    status=EanSearchStatus.SUCCESS.value,
                    product_link=link,
                    redirect_directly_to_store=False,
                )
        elif (
            len(response.html.xpath("//div[@class='sh-pr__product-results']/div")) == 1
            or len(response.html.xpath("//div[@class='sh-dlr__list-result']")) == 1
        ):
            return EanResult(
                status=EanSearchStatus.UNIQUE_STORE.value,
                product_link=self._extract_link_to_store(response),
                redirect_directly_to_store=True,
            )
        return EanResult(
            status=EanSearchStatus.NOT_FOUND.value,
            product_link="",
            redirect_directly_to_store=False,
        )

    @staticmethod
    def _extract_link_to_store(response):
        if store_links_element := response.html.xpath(
            "//a[contains(@href, '/aclk?sa=')]"
        ):
            href = store_links_element[-1].attrs.get("href")
            return GOOGLE_URL + href if GOOGLE_URL not in href else href
        return ""

    @staticmethod
    def _get_store_ref(response):
        if store_ref_element := response.html.xpath(
            "//a[contains(@href, '/aclk?sa=')]",
        ):
            return store_ref_element[-1].text
        return ""

    @staticmethod
    def _get_store_crawler_system(available_systems_dict: dict, store_ref: str):
        if store_item := available_systems_dict.get(store_ref):
            return store_item.get("system", store_item)
        return store_ref

    @staticmethod
    def _get_store_name(available_systems_dict: dict, store_ref: str):
        if store_item := available_systems_dict.get(store_ref):
            return store_item.get("store_name", store_ref)
        return store_ref

    def _send_single_product_to_queue(self, response):
        _available_systems_in_postgres = available_systems()
        store_ref_from_response = self._get_store_ref(response)

        if "R$" not in store_ref_from_response:
            # TODO create a model to it
            product = {
                "product_name_on_google": "",
                "brand": "",
                "ean": self.ean,
                "price": "",
                "store_name": self._get_store_name(
                    _available_systems_in_postgres, store_ref_from_response
                ),
                "store_ref": store_ref_from_response,
                "product_link": self._extract_link_to_store(response),
                "img": "",
                "system": self._get_store_crawler_system(
                    _available_systems_in_postgres, store_ref_from_response
                ),
                "metadata": {
                    "inserted_at": datetime.now(),
                    "updated_at": None,
                    "crawled": False,
                },
            }
            ProductsQueue.insert_products_on_queue(product)
