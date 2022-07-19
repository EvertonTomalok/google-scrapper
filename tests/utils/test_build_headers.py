from src.utils.headers import build_google_headers, build_general_header


def test_build_header(snapshot):
    header = build_google_headers(random=False)
    snapshot.assert_match(header)


def test_build_general_header_no_authority(snapshot):
    header = build_general_header(random=False)
    snapshot.assert_match(header)


def test_build_general_header_with_authority(snapshot):
    header = build_general_header(authority="example.com", random=False)
    snapshot.assert_match(header)


def test_build_general_header_with_origin(snapshot):
    header = build_general_header(origin="https://www.casasbahia.com.br/", random=False)
    snapshot.assert_match(header)
