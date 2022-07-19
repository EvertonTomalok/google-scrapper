from datetime import date
from typing import Union

from src.domain.commands.ean_extractor import get_best_match_from_ean
from src.repositories.product_search import ProductSearchRepository
from src.utils.logger import print_logger


def run_worker_ean_crawler(
    ean_to_search: Union[str, int] = None, search_date: str = None
):
    search_date = search_date or str(date.today())
    operation_result = get_best_match_from_ean(ean_to_search)

    print_logger("\n", operation_result)
    ProductSearchRepository.update_ean(
        ean_to_search,
        search_date,
        operation_result.status,
        operation_result.product_link_on_google,
    )
    print_logger(
        ProductSearchRepository.find_ean_batch(
            {"ean": ean_to_search, "date": "2021-01-26"}, limit=1
        )
    )
