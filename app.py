from cajitos_site import create_app, db
from cajitos_site.models import User, Post, Followers

application = create_app()

if __name__ == '__main__':
    application.run(debug=True)


@application.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Followers': Followers}