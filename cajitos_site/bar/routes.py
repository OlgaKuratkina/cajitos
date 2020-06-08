from flask import request, render_template, current_app
from playhouse.flask_utils import object_list

from cajitos_site.external_apis.cocktails_db import CocktailApi
from cajitos_site.bar import bar
from cajitos_site.utils.db_utils import get_drink_ingredients


@bar.route("/random_cocktail")
def random_cocktail():
    cocktail = CocktailApi().get_random_cocktail()
    return render_template('bar/cocktails.html', drink=cocktail)


@bar.route("/drink_ingredients")
def drink_ingredients():
    all_data = get_drink_ingredients()
    return object_list('bar/drink_ingredients.html', all_data, paginate_by=current_app.config['PER_PAGE'],
                       title='Drink ingredients')


@bar.route("/search")
def search_drink():
    # TODO allow more parameters, allow return list
    ingredient = request.args.get('ingr')
    cocktail = CocktailApi().get_drinks_by_ingredients([ingredient])[0]
    return render_template('bar/cocktails.html', drink=cocktail)

