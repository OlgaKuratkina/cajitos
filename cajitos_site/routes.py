import math

from flask import render_template, request, redirect, url_for, flash, session, abort
from flask_login import login_user, current_user, logout_user, login_required

from cajitos_site.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from cajitos_site.models import VocabularyCard, ExpressionCard, User, Post
from cajitos_site import application, bcrypt
from cajitos_site.utils import get_redirect_target, get_cards, save_picture, get_post_by_id_and_author

PER_PAGE = 3


@application.route("/")
@application.route("/blog_posts")
def blog_posts():
    page = request.args.get('page', 1, type=int)
    total_pages = int(math.ceil(Post.select().count() / PER_PAGE))
    author = request.args.get('author')
    posts = Post.select().order_by(Post.created_at.desc()).paginate(page=page, paginate_by=PER_PAGE)
    if author:
        posts = posts.where(Post.author == author)
    application.logger.warning(posts)
    return render_template(
        'posts.html', title='Blog Posts', posts=posts, author=author, page=page, total_pages=total_pages
    )


@application.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        Post.create(title=form.title.data, content=form.content.data, author=current_user.id, tags='test',
                    category='test')
        flash('Your post has been created!', 'success')
        return redirect(url_for('blog_posts'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@application.route("/post/<int:post_id>")
def post(post_id):
    post = Post.get_or_none(Post.id == post_id)
    if not post:
        abort(404)
    return render_template('post.html', title=post.title, post=post)


@application.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = get_post_by_id_and_author(post_id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.update()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@application.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = get_post_by_id_and_author(post_id)
    post.delete_instance()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('blog_posts'))


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
