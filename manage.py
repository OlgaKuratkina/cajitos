import sys

import click
from flask.cli import with_appcontext
from cajitos_site.utils.utils import get_models_from_module, read_csv
from cajitos_site import models as mod

from cajitos_site import db
from cajitos_site.models import User


def _init_db():
    tables = get_models_from_module(mod)
    db.drop_tables(tables)
    tables = [table for table in tables if table.__name__.lower() not in db.get_tables()]
    if not tables:
        print('All tables are present', db.get_tables())
        return
    db.create_tables(tables)


def fill_vocabulary(filename):
    data = read_csv(filename)
    for row in data:
        mod.VocabularyCard.create(**row)


@click.group()
def cli():
    pass


@cli.command()
@with_appcontext
def shell():
    """Runs a shell in the app context.
    Runs an interactive Python shell in the context of a given
    Flask application. The application will populate the default
    namespace of this shell according to it's configuration.
    This is useful for executing small snippets of management code
    without having to manually configure the application.
    """
    import IPython
    from flask.globals import _app_ctx_stack
    app = _app_ctx_stack.top.app
    banner = 'Python %s on %s\nIPython: %s\nApp: %s %s\nInstance: %s\n' % (
        sys.version,
        sys.platform,
        IPython.__version__,
        app.import_name,
        app.debug and ' [debug]' or '',
        app.instance_path,
    )
    ctx = {'user_model': User, 'db': db}

    # Support the regular Python interpreter startup script if someone
    # is using it.
    # startup = os.environ.get('PYTHONSTARTUP')
    # if startup and os.path.isfile(startup):
    #     with open(startup, 'r') as f:
    #         eval(compile(f.read(), startup, 'exec'), ctx)  # noqa

    ctx.update(app.make_shell_context())
    IPython.embed(config=IPython.get_ipython(), banner1=banner, user_ns=ctx)
    # IPython.start_ipython()


@cli.command()
def init_db():
    _init_db()
    pass


if __name__ == '__main__':
    cli.main()
