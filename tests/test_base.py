import pytest

from cajitos_site import mail
from tests.utils import captured_templates


def test_home(app):
    with captured_templates(app) as templates:
        rv = app.test_client().get('/')
        assert rv.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'blog.html'
        print(context)
        assert len(context['blog']) == 5  # pagination
        # assert {p.author.id for p in context['blog']} == {2}  # Author of the latest 5 blog


def test_base(app):
    rv = app.test_client().get('/blog')
    assert rv.status_code == 200

    print(dir(rv))
    print(rv.stream)


@pytest.mark.skip
def test_service_email(user, app):
    with mail.record_messages() as outbox:
        mail.send_message(subject='testing',
                          body='test',
                          recipients=[user.email])

        assert len(outbox) == 1
        assert outbox[0].subject == "testing"
