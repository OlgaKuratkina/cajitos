from cajitos_site import mail
from tests.utils import captured_templates


def test_home(app):
    with captured_templates(app) as templates:
        rv = app.test_client().get('/')
        assert rv.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'posts.html'
        print(context)
        assert len(context['posts']) == 5  # pagination
        assert {p.author.id for p in context['posts']} == {2}  # Author of the latest 5 posts


def test_base(app):
    rv = app.test_client().get('/blog_posts')
    assert rv.status_code == 200

    print(dir(rv))
    print(rv.stream)


def test_service_email(user, app):
    with mail.record_messages() as outbox:
        mail.send_message(subject='testing',
                          body='test',
                          recipients=[user.email])

        assert len(outbox) == 1
        assert outbox[0].subject == "testing"
