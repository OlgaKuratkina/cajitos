import math

from flask import Blueprint, request, render_template, flash, redirect, url_for, abort, current_app
from flask_login import login_required, current_user

from cajitos_site.posts.forms import PostForm, UpdatePostForm
from cajitos_site.models import Post
from cajitos_site.db_utils import get_post_by_id_and_author

posts = Blueprint('posts', __name__)


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
                    category='test')
        flash('Your post has been created!', 'success')
        return redirect(url_for('posts.blog_posts'))
    return render_template('create_post.html', title='New Post', form=form)


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
        post.update()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form)


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = get_post_by_id_and_author(post_id)
    post.delete_instance()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('posts.blog_posts'))