import json
import urllib.parse

import requests
from flask import current_app, Request
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


def get_google_user_info(req: Request):
    client = WebApplicationClient(current_app.config['GOOGLE_CLIENT_ID'])
    code = req.args.get('code')
    callback_uri = current_app.config.get('GOOGLE_CLIENT_CALLBACK')
    # Find out what URL to hit to get tokens that allow you to ask for things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg['token_endpoint']
    userinfo_endpoint = google_provider_cfg['userinfo_endpoint']
    # Prepare and send a req to get tokens

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=translate_url_https(req.url),
        redirect_url=callback_uri,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(current_app.config.get('GOOGLE_CLIENT_ID'), current_app.config.get('GOOGLE_CLIENT_SECRET')),
    )
    client.parse_request_body_response(json.dumps(token_response.json()))
    # let's find and hit the URL from Google that gives you the user's profile information
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo = requests.get(uri, headers=headers, data=body).json()
    return userinfo