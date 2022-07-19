import pytest
from schematics.exceptions import DataError

from src.models.product import Product


def test_product_ok(snapshot):
    data = {
        "ean": 123456769,
        "sku": "wv12345",
        "product_reference": "tw-1000",
        "url": "https://example.com",
        "status": "S",
        "attribute_name": "voltagem",
        "attribute_value": "110V",
        "seller_name": "Magalu",
        "store_id": 1,
    }

    result = Product(data)
    result.validate()
    snapshot.assert_match(result.to_primitive())


def test_product_ok_with_fields_not_required(snapshot):
    data = {
        "ean": 123456769,
        "sku": "wv12345",
        "url": "https://example.com",
        "store_id": 1,
    }

    result = Product(data)
    result.validate()
    snapshot.assert_match(result.to_primitive())


def test_product_not_ok():
    with pytest.raises(DataError):
        data = {
            "product_reference": "tw-1000",
            "url": "https://example.com",
            "status": "S",
            "attribute_name": "voltagem",
            "attribute_value": "110V",
            "seller_name": "Magalu",
            "store_id": 1,
        }

        result = Product(data)
        result.validate()
