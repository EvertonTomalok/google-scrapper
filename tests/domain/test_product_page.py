import responses

from src.domain.product_page import GoogleProductPage


@responses.activate
def test_product_page(snapshot, google_product_page_response):
    url = (
        "https://www.google.com/shopping/product/13239497633151178800?biw=1324&bih=637#online"
    )

    responses.add(
        responses.Response(method="GET", url=url, status=200, body=google_product_page_response)
    )

    product_page = GoogleProductPage(url).run()
    snapshot.assert_match(product_page)
