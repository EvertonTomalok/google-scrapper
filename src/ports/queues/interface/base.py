from abc import ABC, abstractmethod
from typing import Any


class QueueInterface(ABC):
    @staticmethod
    @abstractmethod
    def send_to_queue(data: Any, *args, **kwargs):
        ...

    @staticmethod
    @abstractmethod
    def get_next(*args, **kwargs):
        ...
