from logging import getLogger
from os import getenv

from src.adapters.postgres.db import PostgresDatabase
from src.models.product import Product
from src.utils.model_validator import validate_and_parse_model

LOGGER_LEVEL = getenv("LOGGER_LEVEL", "DEBUG")

logger = getLogger()
logger.setLevel(LOGGER_LEVEL)


class ProductRepository:
    @staticmethod
    def save(store_table: str, product: dict):
        with PostgresDatabase(store_table, "google") as db:
            if product := validate_and_parse_model(product, Product):
                db.insert_one(
                    fields=list(product.keys()), values=list(product.values()),
                )
                logger.debug(product)
