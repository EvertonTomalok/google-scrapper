import re

import responses

from src.features.systems.magazineluiza import MagazineLuiza


@responses.activate
def test_magazine_luiza_spider(snapshot, magazine_luiza_page_response):
    url = (
        "https://www.magazineluiza.com.br/fogao-4-bocas-electrolux-prata-automatico-com-forno-de-70l-52lxs"
        "/p/bbgjbdjgk0/ed/fogo/?&seller_id=electrolux"
    )

    responses.add(
        responses.Response(
            method="GET",
            url=re.compile(r"https://www.magazineluiza.com.br/.*"),
            status=200,
            body=magazine_luiza_page_response
        )
    )

    product_info = MagazineLuiza(product_url=url).run()
    snapshot.assert_match(product_info)
