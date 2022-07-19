import pytest
import os

cwd = os.getcwd()


def load_fixture(path):
    with open(path) as file:
        return file.read()


@pytest.fixture(scope="module")
def google_search_response_multiple_stores():
    return load_fixture(f"{cwd}/tests/fixtures/google_ean_search.html")


@pytest.fixture(scope="module")
def google_search_response_single_store():
    return load_fixture(f"{cwd}/tests/fixtures/google_ean_search_single_store.html")


@pytest.fixture(scope="module")
def google_search_response_ok():
    return load_fixture(f"{cwd}/tests/fixtures/google_stores_page_ok.html")


@pytest.fixture(scope="module")
def google_search_response_not_found():
    return load_fixture(f"{cwd}/tests/fixtures/google_ean_search_not_found.html")


@pytest.fixture(scope="module")
def google_product_page_response():
    return load_fixture(f"{cwd}/tests/fixtures/google_page_product.html")


@pytest.fixture(scope="module")
def google_stores_page_response():
    return load_fixture(f"{cwd}/tests/fixtures/google_stores_page.html")


@pytest.fixture(scope="module")
def magazine_luiza_page_response():
    return load_fixture(f"{cwd}/tests/fixtures/magazine_luiza_product_page.html")


@pytest.fixture(scope="module")
def ferragens_floresta_page_response():
    return load_fixture(f"{cwd}/tests/fixtures/ferragens_floresta.html")


@pytest.fixture(scope="module")
def json_ad_links():
    return load_fixture(f"{cwd}/tests/fixtures/ad_json_links.txt")
