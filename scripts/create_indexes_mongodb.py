
from src.adapters.mongodb.db import MongoDBDatabase


def ensure_index():
    with MongoDBDatabase("google_stores", "products_to_crawl") as db:
        two_days_in_seconds = 3600 * 24 * 2

        db.create_index(
            [("metadata.inserted_at", 1)],
            "expiration_index",
            expire_after_seconds=two_days_in_seconds,
        )
        db.create_index(
            [("metadata.crawled", 1), ("ean", 1)],
            "crawled_index",
        )

    with MongoDBDatabase("data_quality", "products") as db:
        db.create_index(
            [("url", 1)],
            "products_url_index",
        )

        db.create_index(
            [("ean", 1), ("sku", 1)],
            "products_ean_sku_index",
        )


if __name__ == '__main__':
    print("Starting...")
    ensure_index()
    print("All done!")
