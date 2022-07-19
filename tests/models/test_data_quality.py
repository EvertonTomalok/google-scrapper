import pytest
from schematics.exceptions import DataError

from src.models.dataquality import DataQuality


def test_data_quality_ok(snapshot):
    result = DataQuality(
        {"ean": 1, "product_name": "Cafeteira", "brand": "CADENCE"}
    )

    result.validate()
    snapshot.assert_match(result.to_primitive())


def test_data_quality_not_ok(snapshot):
    with pytest.raises(DataError):
        result = DataQuality({"product_name": "Cafeteira"})
        result.validate()
