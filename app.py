from cajitos_site import create_app, db, cli
from cajitos_site.models import User, Post, Followers, Ingredient, Drink

application = create_app()
cli.register(application)

if __name__ == '__main__':
    application.run()


@application.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Followers': Followers,
            'Ingerdient': Ingredient, 'Drink': Drink}
