import logging
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, current_user, logout_user, login_required

from cajitos_site.forms import RegistrationForm, LoginForm
from cajitos_site.models import VocabularyCard, ExpressionCard, User
from cajitos_site import application, bcrypt, db


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@application.route("/")
def start():
    return render_template('index.html')


@application.route("/blog_posts")
def blog_posts():
    return render_template('posts.html', title='BlackCat', posts=posts)


@application.route("/cards", methods=['POST', 'GET'])
def cards():
    search = None
    if request.method == 'POST':
        search = request.form.get('search_word')
        origin_word = request.form.get('origin_word')
        translation = request.form.get('translation')
        part_speech = request.form.get('part_speech')
        language = request.form.get('language')
        if origin_word and translation and language:
            VocabularyCard.create(origin_word=origin_word, translation_word=translation, origin_language=language,
                                  part_of_speech=part_speech)
    list_cards = get_cards(search)
    return render_template('vocabulary.html', cards=list_cards)


@application.route("/expressions", methods=['POST', 'GET'])
def expressions():
    if request.method == 'POST':
        origin_expression = request.form.get('origin_expression')
        translation_expression = request.form.get('translation_expression')
        category = request.form.get('category')
        language = request.form.get('language')
        if origin_expression and translation_expression and language:
            ExpressionCard.create(origin_expression=origin_expression, translation_expression=translation_expression,
                                  origin_language=language, category=category)
    list_cards = get_cards()
    return render_template('vocabulary.html', cards=list_cards)


@application.route("/runa")
def runa():
    return render_template('runa.html', title="Runa")


@application.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('start'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        User.create(username=form.username.data, email=form.email.data, password=hashed_pass, status='New')
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('blog_posts'))
    return render_template('register.html', title='Register', form=form)


@application.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.select().where(User.email == form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash('You have been logged in!', 'success')
            login_user(user, remember=form.remember.data)
            application.logger.warning('current user %s, session, %s', current_user, session)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('blog_posts'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@application.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('start'))


@application.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


def get_cards(search=None):
    search = f"%{search}%" if search else None
    query = VocabularyCard.select()
    if search:
        query = query.where(VocabularyCard.origin_word ** search)
    return list(query.order_by(VocabularyCard.id.desc()).limit(20))
