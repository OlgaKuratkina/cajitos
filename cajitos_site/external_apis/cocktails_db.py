"""
Cocktails DB API service
"""
import requests

from flask import current_app as app
from marshmallow import schema, fields, EXCLUDE, pre_load, post_load

from cajitos_site.models import Drink


class CocktailApi:
    """
    Cocktail API
    """
    def __init__(self):
        self.base_url = app.config['COCKTAIL_API_URL']
        self.api_key = app.config['COCKTAIL_API_KEY']
        self.api_version = 'v1' if self.api_key == '1' else 'v2'
        self.url = f'{self.base_url}/{self.api_version}/{self.api_key}'
        # https://www.thecocktaildb.com/api/json/v2/9973533/random.php

    def _get(self, path, json=None, **kwargs):
        response = requests.get(
            f'{self.url}/{path}',
            params=kwargs,
            json=json,
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()
        # app.logger.info(data)
        return response.json()

    def get_random_cocktail(self):
        """
        calls /random.php API from cocktail API
        """
        data = self._get('random.php')
        cocktail = data['drinks'][0]
        drink = DrinkSchema().load(cocktail)
        app.logger.info(drink)
        return drink


class DrinkSchema(schema.Schema):
    class Meta:
        unknown = EXCLUDE
    ext_id = fields.Integer(data_key='idDrink')
    name = fields.String(data_key='strDrink')
    is_alcoholic = fields.Boolean(data_key='is_alcoholic', default=True)
    alcohol_category = fields.String(data_key='strAlcoholic')
    instruction = fields.String(data_key='strInstructions')
    category = fields.String(data_key='strCategory')
    glass = fields.String(data_key='strGlass')
    image = fields.String(data_key='strDrinkThumb')
    ingredients = fields.Dict(keys=fields.String(), values=fields.String())

    @pre_load
    def pre_load(self, row, **kwargs):
        row['is_alcoholic'] = (row['strAlcoholic'] == 'Alcoholic')
        row['idDrink'] = int(row['idDrink'])
        row['ingredients'] = self.process_ingredients(row)
        return row

    def process_ingredients(self, row):
        ingredients = list(filter(None, [row[f'strIngredient{i}'] for i in range(1, 16)]))
        measures = list(filter(None, [row[f'strMeasure{i}'] for i in range(1, 16)]))
        return {i: m for i, m in zip(ingredients, measures)}

    @post_load
    def make_drink(self, data, **kwargs):
        if not data:
            return None
        app.logger.info(data)
        return cache_data(Drink, data)


def cache_data(model, data):
    if not data:
        return None
    if model.get_or_none(model.ext_id == data['ext_id']):
        return model.update(**data)
    else:
        return model.create(**data)