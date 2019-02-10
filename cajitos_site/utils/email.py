from flask import current_app, render_template
from flask_mail import Message
from threading import Thread

from cajitos_site import mail

CONFIRM_ACCOUNT_MESSAGE = """You are registering on Cajitos website
To confirm your email address please visit the following link:"""
RESET_PASSWORD_MESSAGE = """You requested password reset for you account on Cajitos website
To reset your password, visit the following link:"""


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    from cajitos_site import application
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(application, msg)).start()


def send_bulk_emails(users, subject, text_body, html_body):
    with mail.connect() as conn:
        for user in users:
            msg = Message(recipients=[user.email],
                          body=text_body or html_body,
                          subject=subject)

            conn.send(msg)


def send_service_email(user, url_link, confirm_account=True):
    sender = current_app.config['MAIL_USERNAME']
    recipients = [user.email]
    if confirm_account:
        message_body = CONFIRM_ACCOUNT_MESSAGE
        subject = 'Confirm your account in Cajitos'
    else:
        message_body = RESET_PASSWORD_MESSAGE
        subject = 'Password Reset Request'
    html_body = render_template('email.service_email.html', user=user, url_link=url_link, message_body=message_body)
    txt_body = render_template('email.service_email.txt', user=user, url_link=url_link, message_body=message_body)
    send_email(subject, sender, recipients, text_body=txt_body, html_body=html_body)
