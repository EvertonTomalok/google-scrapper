import pytest
from schematics.exceptions import DataError

from src.models.stores import StoreModel


def test_stores_ok(snapshot):
    store_data = {
        "store_name": "MAGAZINE LUIZA",
        "store_ref": "Magazine Luiza",
        "store_id": 1,
        "status": "S",
        "platform": "magazineluiza",
        "store_table": "magazine_luiza",
        "seller_default": "Magazine Luiza",
        "url": "https://www.magazineluiza.com.br",
    }

    result = StoreModel(store_data)
    result.validate()
    snapshot.assert_match(result.to_primitive())


def test_stores_status_not_exist(snapshot):
    with pytest.raises(DataError):
        store_data = {
            "store_name": "MAGAZINE LUIZA",
            "store_ref": "Magazine Luiza",
            "store_id": 1,
            "status": "NAO EXISTE",
            "platform": "magazineluiza",
            "store_table": "magazine_luiza",
            "seller_default": "Magazine Luiza",
            "url": "https://www.magazineluiza.com.br",
        }
        result = StoreModel(store_data)
        result.validate()


def test_stores_status_not_ok(snapshot):
    with pytest.raises(DataError):
        store_data = {
            "store_name": "MAGAZINE LUIZA",
            "platform": "magazineluiza",
            "store_table": "magazine_luiza",
            "seller_default": "Magazine Luiza",
            "url": "https://www.magazineluiza.com.br",
        }
        result = StoreModel(store_data)
        result.validate()
