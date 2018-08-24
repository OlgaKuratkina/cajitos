from flask import Flask, render_template, request, jsonify

import peewee as pw
from main.models import VocabularyCard
from main.settings import DB_NAME, DB_USER, DB_HOST, DB_PORT, DB_PASS

application = Flask(__name__)

db = pw.PostgresqlDatabase(
    DB_NAME,
    user=DB_USER,
    host=DB_HOST, port=DB_PORT, password=DB_PASS)
db.create_tables([VocabularyCard])


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


def get_cards():
    list_cards = list(VocabularyCard.select().order_by(VocabularyCard.id.desc()).limit(20))
    return list_cards
