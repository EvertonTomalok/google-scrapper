from typing import List

from src.adapters.postgres.db import PostgresDatabase


def available_systems(stores_list: List[dict] = None):
    if not stores_list:
        with PostgresDatabase("stores", schema="google") as db:
            stores_list = db.find()

    return {store["store_ref"].upper(): store for store in stores_list}
