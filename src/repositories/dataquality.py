from src.adapters.postgres.db import PostgresDatabase
from src.models.dataquality import DataQuality
from src.utils.model_validator import validate_and_parse_model


class DataQualityRepository:
    @staticmethod
    def save(product: dict):
        with PostgresDatabase("data_quality", "google") as db:
            if product := validate_and_parse_model(product, DataQuality):
                db.insert_update(
                    fields=list(product.keys()), values=list(product.values()),
                )
