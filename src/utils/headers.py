from random import choice

from src.utils.ua import build_user_agents

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/87.0.4280.88 Safari/537.36"
)

DEFAULT_SEC_CH_UA = '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"'


def build_google_headers(random=True, cached=True) -> dict:
    """
    Build a header to be used in google requests and return it.
    Use cached=True to not use cache.

    @param random: Bool
    @param cached: Bool
    @return: Dict[str, str]
    """

    user_agents = build_user_agents(cached)

    headers = {
        "authority": "www.google.com",
        "cache-control": "max-age=0",
        "sec-ch-ua": DEFAULT_SEC_CH_UA,
        "sec-ch-ua-mobile": "?0",
        "upgrade-insecure-requests": "1",
        "user-agent": DEFAULT_USER_AGENT,
        "accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/"
            "webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        ),
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-dest": "document",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    if random:
        ua = choice(user_agents)
        headers["sec-ch-ua"] = (
            f'"Google Chrome";v="{ua["version"]}",'
            f' " Not;A Brand";v="99", "Chromium";v="{ua["version"]}"'
        )
        headers["user-agent"] = ua.get("user_agent", "")

    return headers


def build_general_header(
    authority: str = None,
    referer: str = None,
    origin: str = None,
    random: bool = True,
    cached: bool = True,
    min_version: int = 55,
) -> dict:
    """
    Build a header and return it. Use cached=True to not use cache.

    @param authority: Str
    @param referer: Str
    @param origin: Str
    @param random: Bool
    @param cached: Bool
    @param min_version: Int
    @return: Dict[str, str]
    """

    user_agents = build_user_agents(min_version=min_version, cached=cached)

    header = {
        "cache-control": "max-age=0",
        "sec-ch-ua": DEFAULT_SEC_CH_UA,
        "sec-ch-ua-mobile": "?0",
        "upgrade-insecure-requests": "1",
        "user-agent": DEFAULT_USER_AGENT,
        "accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/"
            "webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        ),
        "sec-fetch-site": "cross-site",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-dest": "document",
        "referer": referer or "https://www.google.com/",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    if authority:
        header["authority"] = authority
    if origin:
        header["origin"] = origin

    if random:
        ua = choice(user_agents)
        header["sec-ch-ua"] = (
            f'"Google Chrome";v="{ua["version"]}",'
            f' " Not;A Brand";v="99", "Chromium";v="{ua["version"]}"'
        )
        header["user-agent"] = ua.get("user_agent", "")

    return header


def get_random_ua(min_version=55, cached=True):
    user_agents = build_user_agents(min_version=min_version, cached=cached)
    return choice(user_agents)
