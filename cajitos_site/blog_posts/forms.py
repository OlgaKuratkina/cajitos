from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    legend = 'Create Post'
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    is_hidden = BooleanField('Make post private')
    submit = SubmitField('Post')


class UpdatePostForm(PostForm):
    legend = 'Update Post'


class CommentForm(FlaskForm):
    legend = 'Add Comment'
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Add')
