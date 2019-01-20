from flask import Blueprint, redirect, url_for, flash, render_template, session, request, current_app
from flask_login import current_user, login_user, logout_user, login_required

from cajitos_site import bcrypt
from cajitos_site.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from cajitos_site.models import User
from cajitos_site.utils import generate_random_pass, send_service_email, get_redirect_target, save_picture

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('posts.blog_posts'))
    form = RegistrationForm()
    if form.validate_on_submit():
        password = generate_random_pass()
        # TODO extract to method of the User class
        hashed_pass = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User.create(username=form.username.data, email=form.email.data, password=hashed_pass)
        flash(f'Account created for {form.username.data}!', 'success')
        flash(f'Check your email to confirm your new account', 'success')
        token = user.get_validation_token()
        reset_link = f"{url_for('users.validate_token', token=token, _external=True)}"
        send_service_email(user, reset_link)
        return redirect(url_for('posts.blog_posts'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.select().where(User.email == form.email.data).first()
        if user and user.status != 'Confirmed':
            flash('You need to confirm your account to proceed!', 'info')
        elif user and bcrypt.check_password_hash(user.password, form.password.data):
            flash('You have been logged in!', 'success')
            login_user(user, remember=form.remember.data)
            current_app.logger.info('current user %s, session, %s', current_user, session)
            next_page = get_redirect_target()
            return redirect(next_page) if next_page else redirect(url_for('posts.blog_posts'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('posts.blog_posts'))


@users.route("/account", methods=['GET', 'POST'])
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
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/user_pics/' + current_user.profile_picture)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('posts.blog_posts'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.select().where(User.email == form.email.data).first()
        token = user.get_validation_token()
        reset_link = f"{url_for('users.validate_token', token=token, _external=True)}"
        send_service_email(user, reset_link, confirm_account=False)
        flash('An email has been sent with instructions to complete operation.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def validate_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('posts.blog_posts'))
    user = User.verify_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        # Instead of default implementation with user.is_active
        user.status = 'Confirmed'
        user.save()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('validate_token.html', title='Reset Password', form=form)
