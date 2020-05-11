import peewee as pw
import pytest
from mixer.backend.peewee import mixer
from cajitos_site import db
from cajitos_site import models as mod

from cajitos_site.utils.utils import get_models_from_module


@pytest.fixture(scope='function')
def app():
    from cajitos_site import create_app
    app = create_app(None, 'cajitos_site.settings.test')
    app.app_context().push()
    _init_db(db)
    yield app
    _shutdown_db(db)


def _init_db(db):
    tables = get_models_from_module(mod)
    db.create_tables(tables)
    user1 = mixer.blend(mod.User, email=mixer.RANDOM)
    user2 = mixer.blend(mod.User, email=mixer.RANDOM)
    mixer.cycle(5).blend(mod.Post, author=user1, title=mixer.RANDOM, content=mixer.RANDOM)
    mixer.cycle(5).blend(mod.Post, author=user2, title=mixer.RANDOM, content=mixer.RANDOM)
    mod.Followers.create(following_user=user2, followed_user=user1)


def _shutdown_db(db):
    tables = get_models_from_module(mod)
    db.drop_tables(tables)


@pytest.fixture
def user():
    return mixer.blend(mod.User, username='John', email='john@mail.com', password='jjjj')


# @pytest.fixture(scope='session')
# def db_session(app):
#     from cajitos_site import db
#     db.drop_all()
#     db.create_all()
#     return db
#
#
# @pytest.yield_fixture(scope='function', autouse=True)
# def db(app, db_session):
#     try:
#         yield db_session
#     finally:
#         db_session.session.rollback()
#         table_names = ', '.join('"{0}"'.format(table) for table in db_session.get_tables_for_bind())
#         db_session.engine.execute('TRUNCATE {0} RESTART IDENTITY'.format(table_names))
#         db_session.session.commit()
