from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return render_template('error.html', message="""The requested resource is not here"""), 404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('error.html', message="""You don't have permission to do that (403) """), 403


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('error.html', message="""Oops, something went wrong on our side,
    we are already working on it"""), 500