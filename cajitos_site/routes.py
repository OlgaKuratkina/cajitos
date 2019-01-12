import os

import secrets
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image

from cajitos_site.forms import RegistrationForm, LoginForm, UpdateAccountForm
from cajitos_site.models import VocabularyCard, ExpressionCard, User, Post
from cajitos_site import application, bcrypt, db
from cajitos_site.utils import get_redirect_target


@application.route("/")
@application.route("/blog_posts")
def blog_posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.select().order_by(Post.created_at.desc()).paginate(page=page, paginate_by=5)
    return render_template('posts.html', title='Blog Posts', posts=posts)


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
            application.logger.info('current user %s, session, %s', current_user, session)
            next_page = get_redirect_target()
            return redirect(next_page) if next_page else redirect(url_for('blog_posts'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@application.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('start'))


@application.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile_picture = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.save()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/user_pics/' + current_user.profile_picture)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


def get_cards(search=None):
    search = f"%{search}%" if search else None
    query = VocabularyCard.select()
    if search:
        query = query.where(VocabularyCard.origin_word ** search)
    return list(query.order_by(VocabularyCard.id.desc()).limit(20))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(application.root_path, 'static/images/user_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
