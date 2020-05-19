from cajitos_site.utils.auth_utils import translate_url_https


def test_parse_url():
    uri = """http://www.cajitos.es/users/google_login/callback?code=4%2WiSsqi5uKEPW_tQe_mF7-QISC3g-wbl-
    tPAUnuVSfjuuE6etYLukCkcHHnt-8F2gRiscope=email+profile+https%3A%2F%2Fwww.googleapis.com"""
    result = translate_url_https(uri)

    assert result == """https://www.cajitos.es/users/google_login/callback?code=4%2WiSsqi5uKEPW_tQe_mF7-QISC3g-wbl-
    tPAUnuVSfjuuE6etYLukCkcHHnt-8F2gRiscope=email+profile+https%3A%2F%2Fwww.googleapis.com"""
