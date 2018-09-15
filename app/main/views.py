import markdown2
from flask import render_template, request, redirect, url_for, abort, g
from . import main
from .. import db
from .forms import BlogForm
from ..models import User, Blog, Comment
from flask_login import login_required, current_user
from ..email import mail_message

@main.route('/')
def index():
    '''
    view route page function that returns index page
    '''
    blogs = Blog.get_blogs()

    title = 'Home'
    return render_template('index.html', title = title, blogs = blogs)

@main.route('/admin/dashboard')
@login_required
def dashboard():
    '''
    render the dashboard template for admin
    '''
    if not current_user.is_admin:
        abort(403)
        
    return render_template('dashboard.html', title = "Dashboard")

@main.route('/blog/<int:id>', methods = ["GET", "POST"])
def blog(id):
    '''
    route to display a particular blog
    '''
    # display blog
    blog = Blog.query.get(id)

    # update blog
    if blog is None:
        abort(404)
    format_blog = markdown2.markdown(blog.post, extras = ["code-friendly", "fenced-code-blocks"])

    # get info from comment form
    name = request.args.get('name')
    email = request.args.get('email')
    comment = request.args.get('comment')

    if comment:
        # comment instance
        new_comment = Comment(blog_id = blog.id, name = name, email = email, post_comment = comment)
        # save comment
        new_comment.save_comment()
        return redirect(url_for('.blog', id = blog.id))

    # display comments
    comments = Comment.get_comments(blog.id)

    title = 'Blog post'
    return render_template('blog.html', blog = blog, title = title, comments = comments, format_blog = format_blog)

@main.route('/delete/blog/<int:id>', methods = ["GET", "POST"])
def delete_blog(id):
    blog = Blog.delete_blog(id)

    return redirect(url_for('.index'))

@main.route('/delete/comment/<int:id>', methods = ["GET", "POST"])
def delete_comment(id):
    comment = Comment.delete_comment(id)

    return redirect(url_for('.index'))

@main.route('/blog/new/<int:id>', methods = ["GET", "POST"])
# @login_required
def new_blog(id):
    '''
    view category that returns a form to write a blog post
    '''
    form = BlogForm()
    user = User.query.filter_by(id = id).first()
    if form.validate_on_submit():
        title = form.title.data
        image = form.image.data
        post = form.post.data

        # create blog post instance
        new_blog = Blog(title = title, image_path = image, post = post, user = current_user)

        # save blog
        new_blog.save_blog()

        mail_message('New Post', 'email/update', user.email, user = user)

        return redirect(url_for('.index'))

    title = 'New Blog'
    return render_template('new_blog.html', title = title, blog_form = form)