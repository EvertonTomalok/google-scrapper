import logging
from collections import namedtuple

from dotenv import find_dotenv, load_dotenv
from requests_html import HTMLSession

from src.domain.pipelines.google_run import build_google_default_pipeline
from src.repositories.product_search import ProductSearchRepository
from src.utils.ean import generate_ean_variations
from src.utils.enumerators import EanSearchStatus
from src.utils.headers import build_google_headers

load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

PRODUCT = namedtuple("OPERATION", "status product_link_on_google")
ALLOWED_STATUS = [
    EanSearchStatus.SUCCESS.value,
    EanSearchStatus.MULTIPLE_RESULTS.value,
]


def get_best_match_from_ean(
    ean: str, session: HTMLSession = None, headers: dict = None
) -> PRODUCT:
    session = session or HTMLSession()
    headers = headers or build_google_headers()
    ean_variations = generate_ean_variations(ean)

    GOOGLE_DEFAULT_PIPELINE = build_google_default_pipeline(session, headers)

    for ean in ean_variations:
        result = GOOGLE_DEFAULT_PIPELINE.handle(ean)
        if isinstance(result, dict) and result.get("status") in ALLOWED_STATUS:
            return PRODUCT(
                status=result["status"], product_link_on_google=result["product_link"]
            )
        logger.debug("Not worked!")
    return PRODUCT(status="N", product_link_on_google="")


if __name__ == "__main__":
    eans = {
        0: "12345",  # Invalid
        1: "123456789",  # Invalid
        2: "889894929969",
        3: "8806087526691",
        4: "10343943742",
        5: "7898615982407",
        6: "7909569000281",
        7: "7896020640035",
        8: "7896020640011",
        9: "34264476516",
        10: "34264460379",
        11: "7898221458112",
        12: "7899579413587",
        13: "7891301375019",
        14: "7891356076619",  # SINGLE RESULT
        15: "7893299910296",  # INVALID
        16: "7899885009917",
        17: "7899972112568",
        18: "7898904869815",  # Multiple
        19: "7891114090307",
        20: "7897186893136",
        21: "7898617108027",  # SINGLE RESULT
        22: "7898615982414",
        23: "7898221458402",
        24: "10086632248",  # Multiple
        25: "889894929969",
    }

    # from sys import argv
    # ean_to_search = argv[1] if len(argv) == 2 else eans.get(24)

    # ean_to_search = eans.get(23)
    # operation_result = get_best_match_from_ean(ean_to_search)
    # print("\n", operation_result)
    # ProductSearchRepository.update_ean(
    #     ean_to_search,
    #     "2022-07-18",
    #     operation_result.status,
    #     operation_result.product_link_on_google,
    # )
    #
    # print()
    # print(
    #     ProductSearchRepository.find_ean_batch(
    #         {"ean": ean_to_search, "date": "2022-07-18"}, limit=1
    #     )
    # )

    for i, ean in eans.items():
        print(i)
        get_best_match_from_ean(ean)
