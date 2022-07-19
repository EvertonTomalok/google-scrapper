import re

import responses

from src.domain.stores import GoogleStores
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


@responses.activate
def test_google_stores(snapshot, google_stores_page_response, json_ad_links):
    url = "https://www.google.com/shopping/product/13239497633151178800/online?biw=1324&bih=637"
    method = "GET"

    responses.add(
        responses.Response(method=method, url=url, status=200, body=google_stores_page_response)
    )

    responses.add(
        responses.Response(method=method, url=re.compile(r".*plusbox.*"), status=200, body=json_ad_links)
    )

    stores_with_the_product: GoogleStores = GoogleStores(url)
    stores_with_the_product.run()

    stores = {
        store.name: {
            "price": store.product_price,
            "redirect_link": store.redirect_link,
            "ads": store.more_ads,
        }
        for store in stores_with_the_product.stores
    }
    snapshot.assert_match(stores)
