from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
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
