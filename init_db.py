from mixer.backend.peewee import mixer

from cajitos_site.utils import get_models_from_module
from cajitos_site import models as mod, db


def _init_db():
    # tables = get_models_from_module(mod)
    tables = [mod.VocabularyCard, mod.User, mod.Post, mod.Followers]
    if set(db.get_tables()) == set([table.__name__ for table in tables]):
        return
    db.drop_tables([tables])
    db.create_tables([tables])
    user1 = mixer.blend(mod.User)
    user2 = mixer.blend(mod.User)
    mixer.cycle(5).blend(mod.Post, author=user1)
    mixer.cycle(5).blend(mod.Post, author=user2)
    mod.Followers.create(following_user=user2, followed_user=user1)


if __name__ == '__main__':
    _init_db()
