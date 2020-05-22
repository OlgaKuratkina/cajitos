import six
from google.cloud import translate_v2 as translate
from guess_language import guess_language
from flask_babel import _


def translate_text(target, text):
    """Translates text into the target language.
    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    returns translated text
    """
    if not text and target:
        return _('Please specify text for translation')

    translate_client = translate.Client()
    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')
    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    # result['detectedSourceLanguage'] has source language code

    result = translate_client.translate(
        text, target_language=target)
    return result['translatedText']


def get_language(data):
    language = guess_language(data)
    if language == 'UNKNOWN' or len(language) > 5:
        language = ''
    return language
