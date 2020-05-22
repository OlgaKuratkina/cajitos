import math

from flask import request, render_template, current_app, redirect, url_for
from flask_login import current_user
from peewee import fn
import os
from flask import send_from_directory

from cajitos_site.utils.db_utils import get_cards_words, get_cards_expressions, get_drink_ingredients
from cajitos_site.external_apis.cocktails_db import CocktailApi
from cajitos_site.misc import misc
from cajitos_site.misc.forms import ExpressionForm
from cajitos_site.models import VocabularyCard, ExpressionCard
from cajitos_site.utils.experiment_utils import check_file_works


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
            return redirect(url_for('misc.cards'))
    if request.method == 'POST':
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
            return redirect(url_for('misc.expressions'))
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
    data = check_file_works()
    return render_template('debug.html', data=data)


@misc.route("/random_cocktail")
def random_cocktail():
    cocktail = CocktailApi().get_random_cocktail()
    return render_template('cocktails.html', drink=cocktail)


@misc.route("/drink_ingredients")
def drink_ingredients():
    page = 0
    all_data = get_drink_ingredients()
    total_pages = int(math.ceil(get_drink_ingredients().count() / current_app.config['PER_PAGE']))
    return render_template('drink_ingredients.html', ingredients=all_data, page=page, total_pages=total_pages)


@misc.route("/search")
def search_drink():
    # TODO allow more parameters, allow return list
    ingredient = request.args.get('ingr')
    cocktail = CocktailApi().get_drinks_by_ingredients([ingredient])[0]
    return render_template('cocktails.html', drink=cocktail)


@misc.route("/try")
def try_template():
    return render_template('example_template.html')


@misc.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
