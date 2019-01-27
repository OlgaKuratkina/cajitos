from mixer.backend.peewee import mixer

from cajitos_site.utils import get_models_from_module
from cajitos_site import models as mod, db


def _init_db():
    tables = get_models_from_module(mod)
    # db.drop_tables(tables)
    tables = [table for table in tables if table.__name__.lower() not in db.get_tables()]
    if not tables:
        print('All tables are present', db.get_tables())
        return
    db.create_tables(tables)
    user1 = mixer.blend(mod.User)
    user2 = mixer.blend(mod.User)
    mixer.cycle(5).blend(mod.Post, author=user1)
    mixer.cycle(5).blend(mod.Post, author=user2)
    mod.Followers.create(following_user=user2, followed_user=user1)


if __name__ == '__main__':
    _init_db()
