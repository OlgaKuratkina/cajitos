import peewee as pw
import pytest
from mixer.backend.peewee import mixer
from cajitos_site import models as mod

from cajitos_site.utils import get_models_from_module


@pytest.fixture(scope='session')
def db():
    db = pw.SqliteDatabase('cajitos.db')
    _init_db(db)
    yield db
    _shutdown_db(db)


@pytest.fixture(scope='session')
def app():
    from cajitos_site import create_app
    app = create_app(None, 'cajitos_site.settings.test')
    app.app_context().push()
    return app


def _init_db(db):
    tables = get_models_from_module(mod)
    # db.drop_tables(tables)
    db.create_tables(tables)
    user1 = mixer.blend(mod.User)
    user2 = mixer.blend(mod.User)
    mixer.cycle(5).blend(mod.Post, author=user1)
    mixer.cycle(5).blend(mod.Post, author=user2)
    mod.Followers.create(following_user=user2, followed_user=user1)


def _shutdown_db(db):
    tables = get_models_from_module(mod)
    db.drop_tables(tables)


@pytest.fixture
def user():
    return mixer.blend(mod.User, username='John', email='john@mail.com', password='jjjj')
