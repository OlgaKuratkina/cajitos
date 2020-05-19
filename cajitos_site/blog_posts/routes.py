import math

from cajitos_site.blog_posts import posts
from flask import request, render_template, flash, redirect, url_for, abort, current_app
from flask_login import login_required, current_user

from cajitos_site.blog_posts.forms import PostForm, UpdatePostForm, CommentForm
from cajitos_site.utils.db_utils import get_post_by_id_and_author
from cajitos_site.models import Post, Comment


@posts.route("/")
@posts.route("/blog_posts")
def blog_posts():
    page = request.args.get('page', 1, type=int)
    author = request.args.get('author')
    query = Post.select()
    if author:
        query = query.where(Post.author == author)
    total_pages = int(math.ceil(query.count() / current_app.config['PER_PAGE']))
    posts = query.order_by(Post.created_at.desc()).paginate(page=page, paginate_by=current_app.config['PER_PAGE'])
    return render_template(
        'posts.html', title='Blog Posts', posts=posts, author=author, page=page, total_pages=total_pages
    )


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        Post.create(title=form.title.data, content=form.content.data, author=current_user.id, tags='test',
                    category=form.category.data, is_hidden=form.is_hidden.data)
        flash('Your post has been created!', 'success')
        return redirect(url_for('posts.blog_posts'))
    return render_template('create_entry.html', title='New Post', form=form)


@posts.route("/comment/<int:post_id>/new", methods=['GET', 'POST'])
@login_required
def new_comment(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        Comment.create(post_id=post_id, content=form.content.data, author=current_user.id)
        flash('Your comment has been added!', 'success')
        return redirect(url_for('posts.post', post_id=post_id))
    return render_template('create_entry.html', title='New Comment', form=form)


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
        post.title = form.title.data
        post.content = form.content.data
        post.save()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_entry.html', title='Update Post', form=form)


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = get_post_by_id_and_author(post_id)
    post.delete_instance(recursive=True)
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('posts.blog_posts'))
