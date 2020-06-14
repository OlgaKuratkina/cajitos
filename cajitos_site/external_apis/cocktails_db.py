"""
Cocktails DB API service
"""
import requests

from flask import current_app as app
from marshmallow import schema, fields, EXCLUDE, pre_load, post_load

from cajitos_site.utils.db_utils import cache_data
from cajitos_site.models import Drink, Ingredient


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
        return drink

    def get_ingredients(self):
        """
        gets the list of all ingredients
        """
        data = self._get('list.php?i=list')
        i_list = [el.get('strIngredient1') for el in data['drinks']]
        return i_list

    def get_ingredient(self, idd):
        """
        https://www.thecocktaildb.com/api/json/v1/1/lookup.php?iid=552
        """
        data = self._get(f'lookup.php?iid={idd}')
        data = data['ingredients'][0]
        drink = IngrSchema().load(data)
        return drink

    def search_ingredient(self, name):
        """
        https://www.thecocktaildb.com/api/json/v1/1/search.php?i=vodka
        """
        data = self._get(f'search.php?i={name}')
        data = data['ingredients'][0]
        drink = IngrSchema().load(data)
        return drink

    def get_drinks_by_ingredients(self, ingredients: list):
        """
        https://www.thecocktaildb.com/api/json/v1/1/filter.php?i=Dry_Vermouth,Gin,Anis
        """
        list_str = ','.join(ingredients)
        data = self._get(f'filter.php?i={list_str}')
        data = data['drinks']
        drinks = DrinkSchema().load(data=data, many=True)
        result = []
        for drink in drinks:
            d = cache_data(Drink, drink)
            result.append(d)
        return result


class IngrSchema(schema.Schema):
    __model__ = Ingredient

    class Meta:
        unknown = EXCLUDE
    ext_id = fields.Integer(data_key='idIngredient')
    name = fields.String(data_key='strIngredient')
    is_alcoholic = fields.Boolean(data_key='is_alcoholic', default=True)
    alcohol = fields.String(data_key='strAlcohol', missing='', allow_none=True)
    category = fields.String(data_key='strType', missing='', allow_none=True)
    image = fields.String(data_key='strDrinkThumb', missing='', allow_none=True)
    description = fields.String(data_key='strDescription', missing='', allow_none=True)

    @pre_load
    def pre_load(self, row, **kwargs):
        row['is_alcoholic'] = (row['strAlcohol'] is not None or row['strAlcohol'] == 'Yes')
        row['idIngredient'] = int(row['idIngredient'])
        row['strDrinkThumb'] = f"https://www.thecocktaildb.com/images/ingredients/" \
            f"{row['strIngredient'].lower().replace(' ', '_')}.png"
        return row

    @post_load
    def make_ingr(self, data, **kwargs):
        if not data:
            return None
        app.logger.info(data)
        return cache_data(self.__model__, data)


class DrinkSchema(schema.Schema):
    __model__ = Drink

    class Meta:
        unknown = EXCLUDE
    ext_id = fields.Integer(data_key='idDrink')
    name = fields.String(data_key='strDrink')
    is_alcoholic = fields.Boolean(data_key='is_alcoholic', default=True)
    alcohol_category = fields.String(data_key='strAlcoholic', missing='', allow_none=True)
    instruction = fields.String(data_key='strInstructions')
    category = fields.String(data_key='strCategory', missing='', allow_none=True)
    glass = fields.String(data_key='strGlass', missing='', allow_none=True)
    image = fields.String(data_key='strDrinkThumb', missing='', allow_none=True)
    ingredients = fields.Dict(keys=fields.String(), values=fields.String())

    @pre_load
    def pre_load(self, row, **kwargs):
        row['is_alcoholic'] = (row.get('strAlcoholic') and row.get('strAlcoholic') == 'Alcoholic')
        row['alcohol_category'] = row['is_alcoholic'] or ''
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
        return cache_data(self.__model__, data)
