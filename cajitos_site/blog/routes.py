from playhouse.flask_utils import object_list

from cajitos_site.blog import blog
from flask import request, render_template, flash, redirect, url_for, abort, current_app
from flask_babel import _
from flask_login import login_required, current_user

from cajitos_site.blog.forms import PostForm, UpdatePostForm, CommentForm
from cajitos_site.utils.auth_utils import admin_required
from cajitos_site.utils.db_utils import get_post_by_id_and_author, create_or_update_post
from cajitos_site.models import Post, Comment


@blog.route("/")
@blog.route("/blog")
def posts():
    author = request.args.get('author')
    category = request.args.get('category')
    tag = request.args.get('tag')
    query = Post.select()
    if author:
        query = query.where(Post.author == author)
    if category:
        query = query.where(Post.category == category)
    if tag:
        query = query.where(Post.tags ** f"%{tag}%")
    posts = query.order_by(Post.created_at.desc())
    return object_list(
        'blog/posts.html', posts, paginate_by=current_app.config['PER_PAGE'], title='Blog Posts', preview=True
    )


@blog.route("/comments")
def comments():
    author = request.args.get('author')
    query = Comment.select()
    if author:
        query = query.where(Comment.author == author)
    comments = query.order_by(Comment.created_at.desc())
    return object_list('blog/comments.html', comments, paginate_by=current_app.config['PER_PAGE'], title='Comments')


@blog.route("/post/new", methods=['GET', 'POST'])
@admin_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        create_or_update_post(form)
        flash(_('Your post has been created!'), 'success')
        return redirect(url_for('blog.posts'))
    return render_template('blog/editor.html', title=_('New Post'), form=form)


@blog.route("/comment/<int:post_id>/new", methods=['GET', 'POST'])
@login_required
def new_comment(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        Comment.create(post_id=post_id, content=form.content.data, author=current_user.id)
        flash(_('Your comment has been added!'), 'success')
        return redirect(url_for('blog.post', post_id=post_id))
    return render_template('create_entry.html', title=_('New Comment'), form=form)


@blog.route("/post/<int:post_id>")
def post(post_id):
    post = Post.get_or_none(Post.id == post_id)
    if not post:
        abort(404)
    return render_template('blog/post.html', title=post.title, post=post)


@blog.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@admin_required
def update_post(post_id):
    post = get_post_by_id_and_author(post_id)
    form = UpdatePostForm()
    if form.validate_on_submit():
        create_or_update_post(form, post)
        flash(_('Your post has been updated!'), 'success')
        return redirect(url_for('blog.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.category.data = post.category
        form.is_hidden.data = post.is_hidden
        form.tags.data = post.tags
    return render_template('blog/editor.html', title=_('Update Post'), form=form)


@blog.route("/post/<int:post_id>/delete", methods=['POST'])
@admin_required
def delete_post(post_id):
    post = get_post_by_id_and_author(post_id)
    post.delete_instance(recursive=True)
    flash(_('Your post has been deleted!'), 'success')
    return redirect(url_for('blog.posts'))
