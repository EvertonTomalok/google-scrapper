from typing import List, Type, Union

from src.ports.queues.interface.base import QueueInterface
from src.ports.queues.interface.products_queue import UsingMongo

QUEUE_ADAPTER: Type[QueueInterface] = UsingMongo


class ProductsQueue:
    @staticmethod
    def insert_products_on_queue(data: Union[List[dict], dict]):
        QUEUE_ADAPTER.send_to_queue(data)

    @staticmethod
    def get_next_product_from_queue() -> Union[dict, None]:
        return QUEUE_ADAPTER.get_next()
