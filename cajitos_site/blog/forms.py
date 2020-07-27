from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    legend = _l('Create Post')
    title = StringField(_l('Title'), validators=[DataRequired()])
    content = TextAreaField(_l('Content'), validators=[DataRequired()])
    category = StringField(_l('Category'), validators=[DataRequired()])
    is_hidden = BooleanField(_l('Make private'))
    submit = SubmitField(_l('Post me!'))
    tags = StringField(_l('Tags'), validators=[DataRequired()])


class UpdatePostForm(PostForm):
    legend = _l('Update Post')


class CommentForm(FlaskForm):
    legend = _l('Add Comment')
    content = TextAreaField(_l('Content'), validators=[DataRequired()])
    submit = SubmitField(_l('Add'))
