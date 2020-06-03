import math

import markdown
from playhouse.flask_utils import object_list

from cajitos_site.blog_posts import posts
from flask import request, render_template, flash, redirect, url_for, abort, current_app
from flask_babel import _
from flask_login import login_required, current_user

from cajitos_site.blog_posts.forms import PostForm, UpdatePostForm, CommentForm
from cajitos_site.utils.db_utils import get_post_by_id_and_author
from cajitos_site.models import Post, Comment
from cajitos_site.utils.translate_utils import get_language


@posts.route("/")
@posts.route("/blog_posts")
def blog_posts():
    author = request.args.get('author')
    query = Post.select()
    if author:
        query = query.where(Post.author == author)
    posts = query.order_by(Post.created_at.desc())
    return object_list('posts.html', posts, paginate_by=current_app.config['PER_PAGE'],  title='Blog Posts')


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        language = get_language(form.content.data)
        content = markdown.markdown(form.content.data)
        Post.create(title=form.title.data, content=content, author=current_user.id, tags='test',
                    category=form.category.data, is_hidden=form.is_hidden.data, language=language)
        flash(_('Your post has been created!'), 'success')
        return redirect(url_for('posts.blog_posts'))
    return render_template('_editor.html', title=_('New Post'), form=form)


@posts.route("/comment/<int:post_id>/new", methods=['GET', 'POST'])
@login_required
def new_comment(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        Comment.create(post_id=post_id, content=form.content.data, author=current_user.id)
        flash(_('Your comment has been added!'), 'success')
        return redirect(url_for('posts.post', post_id=post_id))
    return render_template('create_entry.html', title=_('New Comment'), form=form)


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.get_or_none(Post.id == post_id)
    if not post:
        abort(404)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = get_post_by_id_and_author(post_id)
    form = UpdatePostForm()
    if form.validate_on_submit():
        language = get_language(form.content.data)
        post.title = form.title.data
        post.content = markdown.markdown(form.content.data)
        post.category = form.category.data
        post.is_hidden = form.is_hidden.data
        post.language = language
        post.save()
        flash(_('Your post has been updated!'), 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.category.data = post.category
        form.is_hidden.data = post.is_hidden
    return render_template('_editor.html', title=_('Update Post'), form=form)


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = get_post_by_id_and_author(post_id)
    post.delete_instance(recursive=True)
    flash(_('Your post has been deleted!'), 'success')
    return redirect(url_for('posts.blog_posts'))
