import re

import responses
from unittest.mock import patch
from src.domain.ean import GoogleSearchEAN


@responses.activate
def test_extracting_ean_ok(snapshot, google_search_response_ok):
    url = re.compile(r"https://www\.google\.com/search.*")
    method = "GET"
    ean = "7891114090307"

    responses.add(
        responses.Response(method=method, url=url, status=200, body=google_search_response_ok)
    )
    search_ean = GoogleSearchEAN(ean).run()

    snapshot.assert_match(search_ean)


@responses.activate
def test_extracting_ean_multiple_stores(snapshot, google_search_response_multiple_stores):
    url = re.compile(r"https://www\.google\.com/search.*")
    method = "GET"
    ean = "889894929969"

    responses.add(
        responses.Response(method=method, url=url, status=200, body=google_search_response_multiple_stores)
    )
    search_ean = GoogleSearchEAN(ean).run()

    snapshot.assert_match(search_ean)


@responses.activate
@patch.object(GoogleSearchEAN, '_send_single_product_to_queue')
def test_extracting_ean_single(fake_sender, snapshot, google_search_response_single_store):
    url = re.compile(r"https://www\.google\.com/search.*")
    method = "GET"
    ean = "7898617108027"

    fake_sender.return_value = "ok"

    responses.add(
        responses.Response(method=method, url=url, status=200, body=google_search_response_single_store)
    )
    search_ean = GoogleSearchEAN(ean).run()

    snapshot.assert_match(search_ean)


@responses.activate
def test_extracting_ean_not_found(snapshot, google_search_response_not_found):
    url = re.compile(r"https://www\.google\.com/search.*")
    method = "GET"
    ean = "7898617108027123142"

    responses.add(
        responses.Response(method=method, url=url, status=200, body=google_search_response_not_found)
    )
    search_ean = GoogleSearchEAN(ean).run()

    snapshot.assert_match(search_ean)
