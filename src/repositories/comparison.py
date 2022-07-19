from typing import List, Union

from src.adapters.postgres.db import PostgresDatabase
from src.models.comparison import Comparison
from src.utils.model_validator import validate_and_parse_model


class ComparisonRepository:
    @staticmethod
    def save(product_data: Union[dict, List[dict]]):
        with PostgresDatabase("comparison", "google") as db:
            if isinstance(product_data, dict):
                if product := validate_and_parse_model(product_data, Comparison):
                    db.insert_one(
                        fields=list(product.keys()), values=list(product.values()),
                    )
            else:
                list_product_parsed = [
                    product
                    for product in product_data
                    if validate_and_parse_model(product, Comparison)
                ]

                if list_product_parsed:
                    db.insert_many(list_product_parsed)
