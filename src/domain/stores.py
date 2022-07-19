import json
from collections import namedtuple

from requests_html import HTMLSession

from src.domain.base import Base

Store = namedtuple("Store", "name product_price redirect_link more_ads")
GOOGLE_URL = "https://www.google.com"


class GoogleStores(Base):
    def __init__(
        self, stores_link: str, session: HTMLSession = None, headers: dict = None
    ):
        super().__init__(session, headers)
        self.stores_link = stores_link
        self.stores = []

    def run(self):
        response = self._perform_request(
            self.stores_link, method="get", headers=self.headers,
        )
        if not response.ok:
            return False

        self._extract_stores_from_page(response)

        if has_more_stores_url := self._has_more_stores(response):
            self._extract_more_stores(has_more_stores_url)

    def get_max_price(self):
        if len(self.stores) > 0:
            return max(self.stores, key=lambda s: s.product_price)
        raise ValueError("You need to run this Class before to use this method")

    def get_min_price(self):
        if len(self.stores) > 0:
            return min(self.stores, key=lambda s: s.product_price)
        raise ValueError("You need to run this Class before to use this method")

    def _extract_stores_from_page(self, response):
        for tr in response.html.xpath("//tr[@class='sh-osd__offer-row']"):
            store_name = self._extract_store_name_from_tr(tr)
            price = self._extract_price_from_tr(tr)
            redirect_link = self._extract_redirect_link_from_tr(tr)
            more_ads = []

            if ad := tr.xpath(".//a[contains(@data-url, 'plusbox')]", first=True):
                ads_link = GOOGLE_URL + ad.attrs.get("data-url", "") + "&fmt=json"
                ad_response = self._perform_request(
                    ads_link, method="get", headers=self.headers,
                )
                more_ads = self._extract_ads(ad_response)

            self.stores.append(Store(store_name, price, redirect_link, more_ads))

    def _extract_more_stores(self, url_more_stores: str):
        response_more_stores = self._perform_request(
            url_more_stores, method="get", headers=self.headers,
        )

        if not response_more_stores.ok:
            return False

        if more_stores_json := self._parse_json_from_response(response_more_stores):
            try:
                for store in more_stores_json[22][0]:
                    price = store[2]
                    redirect_link = GOOGLE_URL + store[3]
                    store_name = store[4]

                    self.stores.append(
                        Store(
                            store_name,
                            self._parse_price_to_float(price),
                            redirect_link,
                            [],
                        )
                    )
            except Exception as err:
                print(err)

    def _extract_ads(self, ad_response):
        try:
            ad_json = self._parse_json_from_response(ad_response)
            if len(ad_json) < 22:
                return []

            ads = []
            for ad in ad_json[22][0]:
                price = ad[2]
                ad_link = GOOGLE_URL + ad[3]
                ads.append(
                    {"price": self._parse_price_to_float(price), "ad_link": ad_link,}
                )
            return ads
        except Exception as err:
            print(err)
            return []

    @staticmethod
    def _parse_json_from_response(response):
        try:
            return json.loads(
                response.html.text.replace(")]}'", "").replace("\xa0", " ")
            )
        except Exception as err:
            print("JSON PARSE:", err)
            return []

    @staticmethod
    def _extract_store_name_from_tr(tr_element):
        if store_name := tr_element.xpath(
            ".//td/div[@class='sh-osd__merchant-info-container']/a/span[1]", first=True
        ):
            return store_name.text
        return ""

    def _extract_price_from_tr(self, tr_element):
        if price_element := tr_element.xpath(".//td[3]/div/div", first=True):
            price = price_element.text
            return self._parse_price_to_float(price)
        return 0

    @staticmethod
    def _extract_redirect_link_from_tr(tr_element):
        if redirect_link_element := tr_element.xpath(
            ".//td/a[text()='Acessar o site']", first=True
        ):
            if link := redirect_link_element.attrs.get("href"):
                return GOOGLE_URL + link
        return ""

    @staticmethod
    def _has_more_stores(response):
        if button_url := response.html.xpath(
            "//div[@id='sh-fp__pagination-button-wrapper']/button", first=True
        ):
            if more_stores_url := button_url.attrs.get("data-url"):
                return f"{GOOGLE_URL}{more_stores_url}&fmt=json"
        return ""

    @staticmethod
    def _parse_price_to_float(price):
        price = price.replace("R$", "").replace(".", "").replace(",", ".").strip()
        return float(price)
