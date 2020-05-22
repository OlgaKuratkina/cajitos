from flask import render_template
from flask_babel import _
from cajitos_site.errors import errors


@errors.app_errorhandler(404)
def error_404(error):
    return render_template('error.html', message=_("The requested resource is not here")), 404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('error.html', message=_("You don't have permission to do that")), 403


@errors.app_errorhandler(400)
def error_400(error):
    return render_template('error.html', message=_("Not verified ")), 400


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('error.html',
                           message=_("Oops, something went wrong on our side, we are already working on it")), 500
