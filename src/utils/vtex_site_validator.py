import re
from typing import Union

from src.helpers.request import Request
from src.utils.headers import build_general_header


def extract_subdomain_if_is_vtex(url) -> Union[str, None]:
    """
        It crawls the site passed as param, and return subdomain from vtex if site
    use vtex system, else returns None.
    @param url: str
    @return: str or None
    """

    response = Request().perform_request(
        url, method="get", headers=build_general_header(), verify=False,
    )
    return _extract_vtex_subdomain(response)


def _extract_vtex_subdomain(response):
    vtex_subdomain_pattern = r"https://(\w+)\.vteximg.*"

    if script := response.html.xpath(
        "//script[contains(@src, '.vteximg.')]", first=True,
    ):
        url = script.attrs.get("src", "")

        if match := re.search(vtex_subdomain_pattern, url):
            return match.group(1)
    return None
