from datetime import datetime
from typing import Any

from src.adapters.mongodb.db import MongoDBDatabase
from src.ports.queues.interface.base import QueueInterface


class UsingMongo(QueueInterface):
    @staticmethod
    def send_to_queue(data: Any, *args, **kwargs):
        with MongoDBDatabase("google", "products_to_crawl") as db:
            if isinstance(data, list):
                db.insert_many(data)
            else:
                db.insert_one(data)

    @staticmethod
    def get_next():
        with MongoDBDatabase("google", "products_to_crawl") as db:
            return db.find_one_and_update(
                {"metadata.crawled": False},
                {
                    "$set": {
                        "metadata.crawled": True,
                        "metadata.updated_at": datetime.now(),
                    }
                },
            )
