from cajitos_site import application as app
from tests.utils import captured_templates


def test_home():
    with captured_templates(app) as templates:
        rv = app.test_client().get('/')
        assert rv.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'posts.html'
        assert len(context['items']) == 10

def test_base():
    assert True