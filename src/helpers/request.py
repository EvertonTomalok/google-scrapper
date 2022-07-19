from logging import INFO, getLogger
from os import getenv
from typing import Union

import backoff
from requests import Response
from requests_html import HTMLResponse, HTMLSession

from src.utils.headers import build_google_headers, get_random_ua

logger = getLogger()
logger.setLevel(INFO)

REQUEST_MAX_TRIES = getenv("REQUEST_MAX_TRIES", 3)
REQUEST_MAX_TIME = getenv("REQUEST_MAX_TIME", 30)


class Request:
    __tried: bool = None

    def __init__(self, session: HTMLSession = None, headers: dict = None):
        self.session: HTMLSession = session or HTMLSession()
        self.headers: dict = headers or build_google_headers()

    @backoff.on_exception(
        backoff.expo, Exception, max_tries=REQUEST_MAX_TRIES, max_time=REQUEST_MAX_TIME,
    )
    def perform_request(
        self,
        url: str,
        method: str,
        headers: dict = None,
        retry_with_random_user_agent: bool = False,
        use_proxy: bool = False,
        timeout: int = 10,
        **kwargs,
    ) -> Union[Response, HTMLResponse]:
        if method.lower() not in ("get", "post", "put", "delete", "patch"):
            logger.info(f"Method {method} isn't allowed.")
            return self.__build_response_status_500(url, headers)

        headers = headers or self.headers

        # TODO write a module to get an usable proxy
        proxies = {} if not use_proxy else {}

        if self.__tried and retry_with_random_user_agent:
            headers = self._renew_header_with_a_new_user_agent(headers)

        self.__tried = True
        # Getting the method in session instance
        # It could be -> session.get
        #             -> session.post
        #             -> session.put
        #             -> session.patch
        #             -> session.delete
        # and all the other HTTP methods
        session_method = getattr(self.session, method.lower())
        return session_method(
            url, headers=headers, proxies=proxies, timeout=timeout, **kwargs
        )

    @staticmethod
    def __build_response_status_500(url=None, headers=None) -> Response:
        r = Response()
        r.status_code = 500
        r.url = url or ""
        r.headers = headers or {}

        return r

    @staticmethod
    def _renew_header_with_a_new_user_agent(header: dict):
        ua = get_random_ua()
        header["sec-ch-ua"] = (
            f'"Google Chrome";v="{ua["version"]}",'
            f' " Not;A Brand";v="99", "Chromium";v="{ua["version"]}"'
        )
        header["user-agent"] = ua["user_agent"]

        return header
