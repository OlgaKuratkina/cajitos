"""This is replicated in Makefile"""

import os
import click
from app import application


@application.cli.group()
def translate():
    """Translation and localization commands."""
    pass


@translate.command()
@click.argument('lang')
def init(lang):
    """Initialize a new language."""
    if os.system('pybabel extract -F babel.cfg -k _l -o translate_mapping.pot .'):
        raise RuntimeError('extract command failed')
    if os.system(
            'pybabel init -i messages.pot -d cajitos_site/translations -l ' + lang):
        raise RuntimeError('init command failed')
    os.remove('messages.pot')


@translate.command()
def update():
    """Update all languages."""
    if os.system('pybabel extract -F babel.cfg -k _l -o translate_mapping.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel update -i translate_mapping.pot -d cajitos_site/translations'):
        raise RuntimeError('update command failed')
    os.remove('messages.pot')


@translate.command()
def compile():
    """Compile all languages."""
    if os.system('pybabel compile -d cajitos_site/translations'):
        raise RuntimeError('compile command failed')