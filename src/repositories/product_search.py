from datetime import date
from logging import getLogger
from os import getenv
from typing import Union

from src.adapters.postgres.db import PostgresDatabase

logger = getLogger()
logger.setLevel(getenv("LOGGER_LEVEL", "DEBUG"))


class ProductSearchRepository:
    @staticmethod
    def find_ean_batch(filter=None, skip=0, limit=10):
        filter = filter or {"date": str(date.today())}

        with PostgresDatabase("product_search", "google") as db:
            return db.find(filter, skip=skip, limit=limit)

    @staticmethod
    def update_ean(
        ean: Union[int, str], date_filter: Union[str, date], status: str, url: str = ""
    ):
        date_filter = str(date_filter)
        ean = ean

        with PostgresDatabase("product_search", "google") as db:
            return db.update_one(
                where_dict={"ean": ean, "date": date_filter},
                update_dict={"url": url, "status": status.upper()},
            )
