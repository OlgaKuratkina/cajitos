import urllib.parse

import requests
from flask import current_app
from oauthlib.oauth2 import WebApplicationClient

from cajitos_site.settings import GOOGLE_DISCOVERY_URL


def translate_url_https(uri):
    result = urllib.parse.urlparse(uri)
    return result._replace(scheme='https').geturl()


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


def generate_google_auth_request():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg['authorization_endpoint']
    # Use library to construct the request for Google login and provide scopes
    client = WebApplicationClient(current_app.config['GOOGLE_CLIENT_ID'])
    callback_uri = current_app.config.get('GOOGLE_CLIENT_CALLBACK')
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=callback_uri,
        scope=['openid', 'email', 'profile'],
    )
    return request_uri