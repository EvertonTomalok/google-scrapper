from enum import Enum


class EanSearchStatus(Enum):
    SUCCESS = "S"
    UNIQUE_STORE = "U"
    NOT_FOUND = "N"
    MULTIPLE_RESULTS = "M"


class Status(Enum):
    success = "SUCCESS"
    error = "ERROR"
