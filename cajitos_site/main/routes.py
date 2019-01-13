import math

from flask import Blueprint, request, render_template

from cajitos_site import PER_PAGE
from cajitos_site.models import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/blog_posts")
def blog_posts():
    page = request.args.get('page', 1, type=int)
    author = request.args.get('author')
    query = Post.select()
    if author:
        query = query.where(Post.author == author)
    total_pages = int(math.ceil(query.count() / PER_PAGE))
    posts = query.order_by(Post.created_at.desc()).paginate(page=page, paginate_by=PER_PAGE)
    return render_template(
        'posts.html', title='Blog Posts', posts=posts, author=author, page=page, total_pages=total_pages
    )