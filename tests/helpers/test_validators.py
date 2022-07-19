from datetime import date

from freezegun import freeze_time

from src.helpers.validators import parse_model_and_validate
from src.models.comparison import Comparison
from src.models.stores import StoreModel
from src.utils.enumerators import Status


@freeze_time("2021-01-27 12:00:01")
def test_validation_ok(snapshot):
    comparison_data = {
        "ean": 123415,
        "store_id": 1,
        "price_to": 200,
        "date": str(date.today()),
        "hour": "11:20:00"
    }
    result = parse_model_and_validate(comparison_data, Comparison)

    assert result.status == Status.success.value

    snapshot.assert_match(result.status)
    snapshot.assert_match(result.data)


@freeze_time("2021-01-27 12:00:01")
def test_validation_not_ok(snapshot):
    comparison_data = {
        "store_id": 1,
        "price_to": 200,
    }
    result = parse_model_and_validate(comparison_data, Comparison)

    assert result.status == Status.error.value

    snapshot.assert_match(result.status)
    snapshot.assert_match(result.data)


def test_store_validation_ok(snapshot):
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
    result = parse_model_and_validate(store_data, StoreModel)

    assert result.status == Status.success.value

    snapshot.assert_match(result.status)
    snapshot.assert_match(result.data)


def test_store_validation_status_not_exist(snapshot):
    store_data = {
        "store_name": "MAGAZINE LUIZA",
        "store_ref": "Magazine Luiza",
        "store_id": 1,
        "status": "Sem Correspondencia",
        "platform": "magazineluiza",
        "store_table": "magazine_luiza",
        "seller_default": "Magazine Luiza",
        "url": "https://www.magazineluiza.com.br",
    }
    result = parse_model_and_validate(store_data, StoreModel)

    assert result.status == Status.error.value

    snapshot.assert_match(result.status)
    snapshot.assert_match(result.data)
