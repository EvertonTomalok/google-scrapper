from random import randint
from time import sleep

from src.domain.commands.store_spider import execute_spider
from src.helpers.queue_consumers_and_producers import ProductsQueue
from src.utils.logger import DEBUGGING, pprint_logger


def run_worker_product_crawl():
    print("WORKER STARTED!")

    while True:
        next_product = ProductsQueue.get_next_product_from_queue()

        if not next_product:
            sleep(randint(5, 15))
            continue

        result = execute_spider(next_product)

        if DEBUGGING and result:
            for r in result:
                del r["_id"], r["ads"], r["metadata"]

                pprint_logger(r)
