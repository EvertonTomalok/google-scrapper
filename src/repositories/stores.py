from logging import getLogger
from os import getenv

from src.adapters.postgres.db import PostgresDatabase
from src.models.stores import StoreModel
from src.utils.model_validator import validate_and_parse_model
from src.utils.postgres_database import ensure_store_table_is_created

LOGGER_LEVEL = getenv("LOGGER_LEVEL", "DEBUG")

logger = getLogger()
logger.setLevel(LOGGER_LEVEL)


class StoresRepository:
    @staticmethod
    def save(store: dict):
        with PostgresDatabase("stores", "google") as db:
            if store := validate_and_parse_model(store, StoreModel):
                db.insert_one(
                    fields=list(store.keys()), values=list(store.values()),
                )
                ensure_store_table_is_created(
                    database=db, store_table=store["store_table"]
                )
                logger.debug(f"{store}\n\n")

    @staticmethod
    def get_stores(filter=None):
        with PostgresDatabase("stores", "google") as db:
            return db.find(filter)
