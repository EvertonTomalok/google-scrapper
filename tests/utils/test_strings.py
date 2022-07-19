import pytest
from src.utils.strings import sanitize_attribute


@pytest.mark.parametrize("attribute", [
    "200V",
    "220V",
    "110V",
    "127V",
    "BIVOLT",
])
def test_sanitize_attribute(attribute, snapshot):
    snapshot.assert_match(
        sanitize_attribute(attribute)
    )
