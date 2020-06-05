import math

import markdown
from flask import request, render_template, current_app, redirect, url_for, jsonify, flash
from flask_babel import _
from flask_login import current_user
from playhouse.flask_utils import object_list
from playhouse.shortcuts import model_to_dict

from cajitos_site.external_apis.cocktails_db import CocktailApi
from cajitos_site.misc import misc
from cajitos_site.misc.forms import ExpressionForm, VocabularyCardForm, DebugForm
from cajitos_site.models import VocabularyCard, ExpressionCard
from cajitos_site.utils.db_utils import get_cards_words, get_cards_expressions, get_drink_ingredients, get_random_record


@misc.route('/cards', methods=['POST', 'GET'])
def cards():
    search = None
    form = VocabularyCardForm()
    # if request.method == 'POST' and current_user.is_authenticated:
    #     origin_word = request.form.get('origin_word')
    #     translation = request.form.get('translation')
    #     part_speech = request.form.get('part_speech')
    #     language = request.form.get('language')
    #     if origin_word and translation and language:
    #         VocabularyCard.create(origin=origin_word, translation=translation, language=language,
    #                               part_of_speech=part_speech, author=current_user.id)
    #         return redirect(url_for('misc.cards'))
    if request.method == 'POST':
        search = request.form.get('search_word')
    list_cards = get_cards_words(search)
    return render_template('vocabulary.html', cards=list_cards, form=form)


@misc.route('card/new', methods=['GET', 'POST'])
def new_card():
    form = VocabularyCardForm()
    if form.validate_on_submit():
        VocabularyCard.create(origin=form.origin.data, translation=form.translation.data, author=current_user.id,
                              part_of_speech=form.part_speech.data, category=form.category.data,
                              language=form.language.data)
        flash(_('Your word has been added! Try using it in learning'), 'success')
        return redirect(url_for('misc.cards'))
    return render_template('create_entry.html', title=_('Add new word'), legend=_('Add new word'), form=form)


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
    raw = request.args.get('raw')
    card = get_random_record(VocabularyCard)
    if raw:
        json_data = model_to_dict(card)
        return jsonify(json_data)
    return render_template('learn_cards.html', card=card)


@misc.route("/runa")
def runa():
    return render_template('runa.html', title="Runa")


@misc.route("/debug", methods=['POST', 'GET'])
def debug():
    form = DebugForm()
    if form.validate_on_submit():
        current_app.logger.info('submitted!')
        text = form.body.data
        html = markdown.markdown(text, extensions=['codehilite'])
        current_app.logger.info(html)
        return render_template('_editor.html', form=form, data=html)
    return render_template('_editor.html', form=form)


@misc.route("/random_cocktail")
def random_cocktail():
    cocktail = CocktailApi().get_random_cocktail()
    return render_template('cocktails.html', drink=cocktail)


@misc.route("/drink_ingredients")
def drink_ingredients():
    all_data = get_drink_ingredients()
    return object_list('drink_ingredients.html', all_data, paginate_by=current_app.config['PER_PAGE'],
                       title='Drink ingredients')


@misc.route("/search")
def search_drink():
    # TODO allow more parameters, allow return list
    ingredient = request.args.get('ingr')
    cocktail = CocktailApi().get_drinks_by_ingredients([ingredient])[0]
    return render_template('cocktails.html', drink=cocktail)


@misc.route("/try")
def try_template():
    return render_template('example_template.html')
