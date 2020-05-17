import json
from datetime import datetime

import requests
from flask import redirect, url_for, flash, render_template, session, request, current_app
from flask_login import current_user, login_user, logout_user, login_required
from oauthlib.oauth2 import WebApplicationClient

from cajitos_site import bcrypt
from cajitos_site.users import users
from cajitos_site.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from cajitos_site.models import User, load_user
from cajitos_site.utils.email import send_service_email
from cajitos_site.utils.utils import generate_random_pass, get_redirect_target, save_picture, get_google_provider_cfg


@users.before_app_request
def before_app_request():
    if current_user.is_authenticated:
        current_app.logger.warn('User last_seen has been updated!')
        current_user.last_seen = datetime.utcnow()
        current_user.save()  # TODO call to save will change modified_at field


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


@users.route('/google_login')
def google_login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg['authorization_endpoint']

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    client = WebApplicationClient(current_app.config['GOOGLE_CLIENT_ID'])
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@users.route("/google_login/callback")
def callback():
    # Get authorization code Google sent back to you
    client = WebApplicationClient(current_app.config['GOOGLE_CLIENT_ID'])
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(current_app.config('GOOGLE_CLIENT_ID'), current_app.config('GOOGLE_CLIENT_SECRET')),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    if not load_user(unique_id):
        user = User.create(
            google_id=unique_id, username=users_name, email=users_email, password='', profile_picture=picture
        )
        login_user(user)

        # Send user back to homepage
        return redirect(url_for("/"))


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
        current_user.about_me = form.about_me.data
        current_user.save()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
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
