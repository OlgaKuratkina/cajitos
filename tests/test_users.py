import json

import pytest

from cajitos_site import mail
from cajitos_site.models import User
from tests.utils import captured_templates


@pytest.mark.skip
def test_user_register(app):
    with captured_templates(app) as templates, mail.record_messages() as outbox:
        payload = dict(username='userB', email='userb@dom.com', submit='Sign Up')
        resp = app.test_client().post('/users/register', data=json.dumps(payload), follow_redirects=True)

        template, context = templates[0]
        print(resp.json)
        user = User.select().where(User.email == 'userb@dom.com').first()
        print(context)
        users = User.select().where(User.email == 'userb@dom.com').get()
        print(users)
        assert resp.status_code == 200
        assert len(outbox) == 1
