from os import getenv
from typing import List


def generate_ean_variations(ean: str) -> List[str]:
    max_ean_length = int(getenv("MAX_EAN_LENGTH", 13))
    min_ean_length = int(getenv("MIN_EAN_LENGTH", 8))

    ean = ean.lstrip("0")
    ean_length = len(ean)

    if ean_length < min_ean_length:
        return []

    num_variations = max_ean_length - ean_length if ean_length <= max_ean_length else 0
    ean_variations = [
        f"{'0' * number_zeros}{ean}" for number_zeros in range(0, num_variations + 1)
    ]

    return ean_variations
