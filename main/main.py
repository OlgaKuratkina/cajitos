from flask import Flask, render_template, request

from main.models import VocabularyCard

application = Flask(__name__)


@application.route("/")
def start():
    return render_template('index.html')


@application.route("/cards", methods=['POST', 'GET'])
def cards():
    if request.method == 'POST':
        origin_word = request.form.get('origin_word')
        translation = request.form.get('translation')
        part_speech = request.form.get('part_speech')
        language = request.form.get('language')
        if origin_word and translation and language:
            VocabularyCard.create(origin_word=origin_word, translation_word=translation, origin_language=language,
                                  part_of_speech=part_speech)
    list_cards = get_cards()
    return render_template('vocabulary.html', cards=list_cards)


@application.route("/runa")
def runa():
    return render_template('runa.html')


def get_cards():
    list_cards = list(VocabularyCard.select().order_by(VocabularyCard.id.desc()).limit(20))
    return list_cards
