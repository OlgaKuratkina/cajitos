from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import TextAreaField, SubmitField, SelectField, StringField
from wtforms.validators import DataRequired, Length


class ExpressionForm(FlaskForm):
    legend = 'Expressions Vocabulary'
    origin_expression = TextAreaField(
        'origin_expression', validators=[DataRequired(), Length(min=5, max=120)]
    )
    translation_expression = TextAreaField(
        'translation_expression', validators=[DataRequired(), Length(min=5, max=120)]
    )
    category = TextAreaField('category')
    language = TextAreaField('language', validators=[DataRequired(), Length(min=2, max=2)])
    submit = SubmitField('Add')


class VocabularyCardForm(FlaskForm):
    legend = 'Add your word, use it for cards'
    origin = StringField(
        _l('Word'),
        # description=_l('Enter your word in a foreign language'),
        validators=[DataRequired(), Length(min=5, max=120)]
    )
    translation = StringField(
        _l('Translation'),
        # description=_l('Enter translation for the word'),
        validators=[DataRequired(), Length(min=5, max=120)]
    )
    part_speech = SelectField(_l('Part of the speech'), choices=[
        ('noun', 'noun'), ('pronoun', 'pronoun'), ('verb', 'verb'), ('adjective', 'adjective'),
        ('adverb', 'adverb'), ('preposition', 'preposition'), ('conjunction', 'conjunction'),
        ('interjection', 'interjection')
    ])
    category = StringField('Category')
    language = SelectField('Language', choices=[('es', 'es'), ('ru', 'ru'), ('en', 'en')])
    submit = SubmitField('Add')


class DebugForm(FlaskForm):
    body = TextAreaField('Enter your markdown')
    submit = SubmitField('Submit')

