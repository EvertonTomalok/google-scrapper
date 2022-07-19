import responses

from src.utils.vtex_site_validator import extract_subdomain_if_is_vtex


@responses.activate
def test_is_vtex_site(snapshot, ferragens_floresta_page_response):
    url = "https://www.ferragensfloresta.com.br/"
    responses.add(
        responses.Response(method="GET", url=url, status=200, body=ferragens_floresta_page_response)
    )
    subdomain = extract_subdomain_if_is_vtex(url)

    snapshot.assert_match(subdomain)


@responses.activate
def test_is_not_vtex_site(snapshot, magazine_luiza_page_response):
    url = "https://www.magazine_luiza.com.br/"
    responses.add(
        responses.Response(method="GET", url=url, status=200, body=magazine_luiza_page_response)
    )
    subdomain = extract_subdomain_if_is_vtex(url)

    snapshot.assert_match(subdomain)
