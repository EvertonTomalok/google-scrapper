import json
from copy import deepcopy
from typing import List, Union

from bs4 import BeautifulSoup

from src.features.systems.base import SystemTemplate
from src.utils.headers import build_general_header
from src.utils.strings import normalize_text, sanitize_attribute


class ViaVarejo(SystemTemplate):
    system = "viavarejo"
    base_url = "https://www.viavarejo.com.br"

    _available_authority = {
        "casasbahia": "www.casasbahia.com.br",
        "extra": "www.extra.com.br",
        "pontofrio": "www.pontofrio.com.br",
    }

    _system_as_seller = {
        "casasbahia": "Casas Bahia",
        "extra": "Extra",
        "pontofrio": "Ponto Frio",
    }

    def __init__(self, product_url: str, system_name: str):
        super().__init__(product_url, force_visit_page=True)
        self.system_name: str = system_name
        self.headers: dict = build_general_header(
            authority=self._available_authority.get(system_name), random=True
        )

        self.store_url: str = (
            f"https://pdp-api.{system_name}.com.br/api/v2/sku/"
            "{sku}/price/source/CB?utm_medium=Cpc&device_type=DESKTOP"
        )
        # Auxiliary attributes
        self._skus_list: List[dict] = []
        self._json_next_data: dict = {}
        self._product_statement: dict = {}

    def run(self) -> List[dict]:
        product_variations = []

        self.visit_page(
            self.product_url,
            "GET",
            headers=self.headers,
            use_proxy=True,
            retry_with_random_user_agent=True,
        )

        info = self._set_info_product_from_last_response_in_cache()

        for sku in self.sku:
            info_copy = deepcopy(info)
            info_copy["sku"] = str(sku)
            info_copy["voltage"] = self._get_attribute(sku)
            info_copy["url"] = self._get_product_url_from_sku_list(self._skus_list, sku)
            product_variations.append(info_copy)

        special_header = {
            "accept": "application/json, text/plain, */*",
            "x-correlation-id": "69c9a49c-57c4-4404-80cb-fa5dcdf74556",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
        }

        self.headers.update(special_header)
        self.visit_page(
            self.store_url.format(sku=self.sku[0]),
            "GET",
            headers=self.headers,
            use_proxy=True,
            retry_with_random_user_agent=True,
        )

        for product in product_variations:
            product["seller_name"] = self.seller_name

        return product_variations

    @property
    def sku(self) -> List[str]:
        if not self._skus_list:
            try:
                self._skus_list = self.product_statement["product"]["skus"]
            except KeyError:
                print("Couldn't find skus")
        return self._get_skus(self._skus_list)

    @property
    def voltage(self) -> str:
        # Not used
        return ""

    @property
    def model(self) -> str:
        return ""

    @property
    def color(self) -> str:
        # TODO get color on ViaVarejo
        return ""

    @property
    def product_name(self) -> str:
        if not self._product_name:
            try:
                self._product_name = self.product_statement["product"]["name"]
            except KeyError:
                print("Couldn't find brand")
        return self._product_name

    @property
    def description(self) -> Union[str, None]:
        if not self._description:
            try:
                description: str = self.product_statement["product"]["description"]
                self._description = self._get_text_from_soup(description)
            except KeyError:
                print("Couldn't find brand")
        return self._description

    @property
    def brand(self) -> str:
        if not self._brand:
            try:
                self._brand = normalize_text(
                    self.product_statement["product"]["brand"]["name"]
                )
            except KeyError:
                print("Couldn't find brand")
        return self._brand

    @property
    def image(self) -> str:
        if not self._image:
            try:
                self._image = self.product_statement["sku"]["images"][0]["url"]
            except KeyError:
                print("Couldn't find image")
        return self._image

    @property
    def url(self) -> str:
        if not self._url:
            self._url = self._last_response.request.url.split("?")[0]
        return self._url

    @property
    def seller_name(self) -> str:
        for seller in self._last_response.json()["sellers"]:
            if seller["elected"] is True:
                seller_name = seller["name"]

                if seller_name == "Casas Bahia":
                    return self._system_as_seller.get(self.system_name)
                return normalize_text(seller_name.replace(" & ", " e "))
        return ""

    # Additional properties
    @property
    def json_next_data(self) -> dict:
        if not self._json_next_data:
            if next_data_script := self._last_response.html.xpath(
                "//script[@id='__NEXT_DATA__']", first=True
            ):
                self._json_next_data = json.loads(next_data_script.text)
        return self._json_next_data

    @property
    def product_statement(self) -> dict:
        if not self._product_statement:
            self._product_statement = self.json_next_data["props"]["initialState"][
                "Product"
            ]
        return self._product_statement

    # Other Methods
    @staticmethod
    def _get_skus(skus_list: List[dict]):
        return [element.get("id", "") for element in skus_list]

    def _get_attribute(self, sku: str):
        """
            Find the attribute in page.
        @param sku: str
        @return: str
        """

        spec_group = self.product_statement["product"].get("specGroups", [])
        sku_list = self.product_statement["product"].get("skus", [])

        if attribute_from_sku_list := self._get_attribute_from_sku_list(sku_list, sku):
            return attribute_from_sku_list
        elif attribute := self._get_attribute_from_technical_specification(spec_group):
            return attribute
        return ""

    @staticmethod
    def _get_attribute_from_technical_specification(json_properties):
        """
            Get attribute from technical specification from props __next_data__ script
        json properties is like:

        "specGroups": [
            {
                "name":"Características",
                "specs":[
                    {
                        "name":"Função impressora",
                        "value":"Sim"
                    },
                    ...
                ]
            },
            {
                "name":"Especificações Técnicas",
                "specs":[
                    {
                        "name":"Cor",
                        "value":"preto"
                    },
                    {
                        "name":"Tensão/Voltagem",
                        "value":"bivolt"
                    },
                    ...
                ]
            }
        ]

        @param json_properties:
        @return:
        """
        for element in json_properties:
            if element.get("name", "") == "Especificações Técnicas":
                for spec in element.get("specs", []):
                    if spec.get("name") == "Tensão/Voltagem":
                        return sanitize_attribute(spec.get("value", ""))
        return ""

    @staticmethod
    def _get_attribute_from_sku_list(sku_list: [List[dict]], sku: str):
        """
            Get the attribute from skus_list, how is called and set by the 'sku'
        property.
            The sku_list is a list of elements present in the product page, in a script
        tag with id 'next_data', and look like it:

            [{'id': 50004230,
              'name': '110V',
              'link': 'https://produto.casasbahia.com.br/50004230'},
             {'id': 50004231,
              'name': '220V',
              'link': 'https://produto.casasbahia.com.br/50004231'}]
        @param sku_list: [List[dict]]
        @param sku: str
        @return: str
        """
        for element in sku_list:
            if element.get("id") == sku and (
                element.get("name", "").endswith("V")
                or element.get("name", "").lower == "bivolt"
            ):
                return sanitize_attribute(element.get("name", ""))
        return ""

    @staticmethod
    def _get_product_url_from_sku_list(_skus_list: List[dict], sku: str):
        """
            Get the link of the product from skus_list, how is called and set by
        the 'sku' property. The sku_list is a list of elements present in the
        product page, in a script tag with id 'next_data', and look like it:

            [{'id': 50004230,
              'name': '110V',
              'link': 'https://produto.casasbahia.com.br/50004230'},
             {'id': 50004231,
              'name': '220V',
              'link': 'https://produto.casasbahia.com.br/50004231'}]

        @param _skus_list: List[Dict]
        @param sku: str
        @return: str
        """
        for element in _skus_list:
            if element.get("id") == sku:
                return element.get("link", "")
        return ""

    def _set_info_product_from_last_response_in_cache(self) -> dict:
        return {
            "product_name": normalize_text(self.product_name),
            "model": self.model,
            "brand": normalize_text(self.brand),
            "description": normalize_text(self.description),
            "image": self.image,
            "color": self.color,
        }

    @staticmethod
    def _get_text_from_soup(tag_text: str):
        soup = BeautifulSoup(tag_text, "lxml")
        return soup.text
