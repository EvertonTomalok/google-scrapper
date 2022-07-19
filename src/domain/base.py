from abc import ABC, abstractmethod
from logging import INFO, getLogger
from typing import Union

from requests import Response
from requests_html import HTMLResponse, HTMLSession

from src.helpers.request import Request

logger = getLogger()
logger.setLevel(INFO)


class Base(ABC):
    def __init__(self, session: HTMLSession = None, headers: dict = None):
        self.session: HTMLSession = session
        self.headers: dict = headers

    @abstractmethod
    def run(self, *args, **kwargs):
        ...

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
