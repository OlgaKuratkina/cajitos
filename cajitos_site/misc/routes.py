import math

from flask import request, render_template, current_app, redirect, url_for
from flask_login import current_user
from peewee import fn

from cajitos_site.external_apis.cocktails_db import CocktailApi
from cajitos_site.misc import misc
from cajitos_site.misc.forms import ExpressionForm
from cajitos_site.models import VocabularyCard, ExpressionCard
from cajitos_site.db_utils import get_cards_words, get_cards_expressions


@misc.route("/cards", methods=['POST', 'GET'])
def cards():
    search = None
    if request.method == 'POST' and current_user.is_authenticated:
        origin_word = request.form.get('origin_word')
        translation = request.form.get('translation')
        part_speech = request.form.get('part_speech')
        language = request.form.get('language')
        if origin_word and translation and language:
            VocabularyCard.create(origin=origin_word, translation=translation, language=language,
                                  part_of_speech=part_speech, author=current_user.id)
    elif request.method == 'POST':
        search = request.form.get('search_word')
    list_cards = get_cards_words(search)
    return render_template('vocabulary.html', cards=list_cards)


@misc.route("/expressions", methods=['POST', 'GET'])
def expressions():
    page = request.args.get('page', 1, type=int)
    form = ExpressionForm()
    if request.method == 'POST' and current_user.is_authenticated:
        origin_expression = request.form.get('origin_expression')
        translation_expression = request.form.get('translation_expression')
        category = request.form.get('category')
        language = request.form.get('language')
        if origin_expression and translation_expression and language:
            ExpressionCard.create(origin_expression=origin_expression, translation_expression=translation_expression,
                                  origin_language=language, category=category, author=current_user.id)
            return redirect(url_for('things.expressions'))
    # TODO make pretty
    list_cards = get_cards_expressions(page=page)
    total_pages = int(math.ceil(get_cards_expressions().count() / current_app.config['PER_PAGE']))
    return render_template('expressions.html', title='Vocabulary of expressions', form=form, cards=list_cards,
                           page=page, total_pages=total_pages)


@misc.route("/random_card")
def random_card():
    card = VocabularyCard.select().order_by(fn.Random()).limit(1).first()
    return render_template('learn_cards.html', card=card)


@misc.route("/runa")
def runa():
    return render_template('runa.html', title="Runa")


@misc.route("/debug")
def debug():
    data = []
    return render_template('debug.html', data=data)


@misc.route("/random_cocktail")
def random_cocktail():
    cocktail = CocktailApi().get_random_cocktail()
    return render_template('cocktails.html', drink=cocktail)
