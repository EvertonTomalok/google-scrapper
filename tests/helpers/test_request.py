import re

import responses

from src.helpers.request import Request


@responses.activate
def test_request_ok(snapshot):
    responses.add(
        responses.Response(
            method="GET",
            url=re.compile(r".*example\.com\.br"),
            status=200,
            body="ok"
        )
    )
    requester = Request()
    response = requester.perform_request(url="https://www.example.com.br", method="GET")
    snapshot.assert_match(response.text)

    assert response.ok


def test_request_not_ok():
    requester = Request()
    response = requester.perform_request(url="https://www.example.com.br", method="METHOD DOESN'T EXIST")

    assert not response.ok
