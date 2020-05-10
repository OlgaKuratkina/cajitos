from cajitos_site.external_apis.cocktails_db import CocktailApi
from tests.utils import captured_templates


def test_random_drink(app):
    with captured_templates(app) as templates:
        resp = app.test_client().get('/things/random_cocktail')

        template, context = templates[0]
        assert resp.status_code == 200
        assert template.name == 'cocktails.html'

        cocktail = CocktailApi().get_random_cocktail()
        assert isinstance(cocktail.ingredients, dict)
        assert cocktail.name
        assert cocktail.ingredients
