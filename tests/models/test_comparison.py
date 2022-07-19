import datetime

import pytest
from schematics.exceptions import DataError

from src.models.comparison import Comparison
from freezegun import freeze_time


@freeze_time("2021-01-27 10:00:01")
def test_comparison_valid_complete(snapshot):
    result = Comparison(
        {
            "ean": "121341",
            "store_id": 1,
            "price_to": 2,
            "date": datetime.datetime.now(),
            "hour": datetime.datetime.now().hour
        }
    )

    result.validate()
    snapshot.assert_match(result.to_primitive())


def test_comparison_invalid_not_ean(snapshot):
    with pytest.raises(DataError):
        result = Comparison(
            {
                "store_id": 1,
                "price_to": 2,
                "date": datetime.datetime.now(),
                "hour": datetime.datetime.now().hour
            }
        )
        result.validate()


def test_comparison_invalid_not_items(snapshot):
    with pytest.raises(DataError):
        result = Comparison(
            {
                "date": datetime.datetime.now(),
                "hour": datetime.datetime.now().hour
            }
        )
        result.validate()
