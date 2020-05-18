import logging
import os

from logging.handlers import RotatingFileHandler, SMTPHandler


def configure_app(application):
    if not application.debug:
        # OAuth 2 client setup
        # application.oauth_client = WebApplicationClient(application.config['GOOGLE_CLIENT_ID'])

        # if application.config.get('MAIL_SERVER'):
        #     auth = None
        #     if application.config.get('MAIL_USERNAME') or application.config.get('MAIL_PASSWORD'):
        #         auth = (application.config['MAIL_USERNAME'], application.config['MAIL_PASSWORD'])
        #     secure = None
        #     # if application.config['MAIL_USE_TLS']:
        #     #     secure = ()
        #     mail_handler = SMTPHandler(
        #         mailhost=(application.config['MAIL_SERVER'], application.config['MAIL_PORT']),
        #         fromaddr='no-reply@' + application.config['MAIL_SERVER'],
        #         toaddrs=application.config['OWNERS'], subject='Cajitos Failure',
        #         credentials=auth, secure=secure)
        #     mail_handler.setLevel(logging.ERROR)
        #     application.logger.addHandler(mail_handler)

            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/cajitos.log', maxBytes=10240,
                                               backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            application.logger.addHandler(file_handler)
            application.logger.setLevel(logging.INFO)
            application.logger.info('Cajitos startup')
