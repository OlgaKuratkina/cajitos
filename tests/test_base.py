# from cajitos_site import application as app
from tests.utils import captured_templates


def test_home(app):
    with captured_templates(app) as templates:
        rv = app.test_client().get('/')
        assert rv.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'posts.html'
        print(context)
        for p in context['posts']:
            print(p)


def test_base(app):
    rv = app.test_client().get('/blog_posts')
    assert rv.status_code == 200

    print(dir(rv))
    print(rv.stream)