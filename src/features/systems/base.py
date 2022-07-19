from abc import ABC, abstractmethod
from typing import List, Union

from requests import Response
from requests_html import HTMLResponse, HTMLSession

from src.helpers.request import Request
from src.utils.strings import normalize_text


class SystemTemplate(ABC):
    # Metadata from Class
    system: str = None
    base_url: str = None

    # Response that could be used to help on the properties
    _last_response: HTMLResponse = None

    def __init__(
        self,
        product_url: str,
        session: HTMLSession = None,
        headers: dict = None,
        force_visit_page: bool = False,
    ):
        self.product_url = product_url
        self.session: HTMLSession = session
        self.headers: dict = headers

        # Properties
        self._product_name: str = ""
        self._sku: str = ""
        self._attribute: str = ""
        self._model: str = ""
        self._description: str = ""
        self._brand: str = ""
        self._image: str = ""
        self._url: str = ""
        self._seller_name: str = ""
        self._color: str = ""

        # Auxiliary param
        self.__force_visit = force_visit_page

    def run(self, *args, **kwargs) -> List[dict]:
        self.visit_page(self.product_url, method="GET", headers=self.headers)
        return [self.to_dict()]

    def visit_page(
        self, url: str, method: str = "GET", **kwargs
    ) -> Union[Response, HTMLResponse]:
        response = self._perform_request(url, method, **kwargs)
        self._last_response = response
        return response

    @property
    @abstractmethod
    def sku(self) -> str:
        return self._sku

    @property
    @abstractmethod
    def voltage(self) -> str:
        return self._attribute

    @property
    @abstractmethod
    def color(self) -> str:
        return self._color

    @property
    @abstractmethod
    def model(self) -> str:
        return self._model

    @property
    @abstractmethod
    def product_name(self) -> str:
        return self._product_name

    @property
    @abstractmethod
    def description(self) -> str:
        return self._description

    @property
    @abstractmethod
    def brand(self) -> str:
        return self._brand

    @property
    @abstractmethod
    def image(self) -> str:
        return self._image

    @property
    @abstractmethod
    def url(self) -> str:
        return self._url

    @property
    @abstractmethod
    def seller_name(self) -> str:
        return self._seller_name

    def to_dict(self):
        if self.__force_visit:
            self._force_visit_page()

        return {
            "product_name": normalize_text(self.product_name),
            "sku": self.sku,
            "description": self.description or "",
            "brand": normalize_text(self.brand),
            "model": self.model,
            "voltage": normalize_text(self.voltage),
            "color": normalize_text(self.color),
            "image": self.image,
            "url": self.url,
            "seller_name": normalize_text(self.seller_name),
        }

    def _perform_request(
        self,
        url: str,
        method: str,
        headers: dict = None,
        retry_with_random_user_agent: bool = False,
        use_proxy: bool = False,
        timeout: int = 10,
        **kwargs,
    ) -> Union[Response, HTMLResponse]:
        return Request(self.session, self.headers).perform_request(
            url=url,
            method=method,
            headers=headers,
            retry_with_random_user_agent=retry_with_random_user_agent,
            use_proxy=use_proxy,
            timeout=timeout,
            **kwargs,
        )

    def _force_visit_page(self):
        if not self._last_response:
            self.visit_page(self.product_url, method="GET", headers=self.headers)
