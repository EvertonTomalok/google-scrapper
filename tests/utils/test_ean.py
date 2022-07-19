import pytest

from src.utils.ean import generate_ean_variations


@pytest.mark.parametrize(
    "ean",
    ["88888888", "999999999", "1010101010", "11111111111", "121212121212", "1313131313131"]
)
def test_generate_ean_variations_allowed(ean, snapshot):
    ean_variations = generate_ean_variations(ean)
    snapshot.assert_match(ean_variations)


@pytest.mark.parametrize(
    "ean",
    ["1", "12", "123", "1234", "12345", "123456", "1234567"]
)
def test_generate_ean_variations_not_allowed(ean, snapshot):
    ean_variations = generate_ean_variations(ean)
    snapshot.assert_match(ean_variations)
