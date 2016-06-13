from flask import render_template, flash, redirect, url_for
from app import app, db
from .forms import CommentForm
from .models import BlogPost, Comment, CodeProject
from config import CODEPROJECTS_PER_PAGE, BLOGPOSTS_PER_PAGE
from sqlalchemy import desc

# Sets up the url and functions that load html pages

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    # For sidebar
    b = BlogPost.query.order_by(desc(BlogPost.timestamp)).limit(5).all()
    # url = url_for('blog_post', blog_title=b[0].title_no_spaces)
    # b = BlogPost(title='yes')
    if b is None:
        return redirect('/about')            # redirect to 404
    return render_template('index.html',
                           blog_post=b[0],
                           blog_posts=b)

@app.route('/about')
def about():
    # For sidebar
    b = BlogPost.query.order_by(desc(BlogPost.timestamp)).limit(5).all()
    return render_template('about.html',
                           blog_posts=b)

@app.route('/base')
def base():
    # For sidebar
    b = BlogPost.query.order_by(desc(BlogPost.timestamp)).limit(5).all()
    return render_template('base.html',
                           blog_posts=b)

# http://exploreflask.readthedocs.io/en/latest/views.html
@app.route('/blog')
@app.route('/blog/<page>')
def blog(page=1):
    # For sidebar
    b = BlogPost.query.order_by(desc(BlogPost.timestamp)).limit(5).all()
    main = BlogPost.query.order_by(desc(BlogPost.timestamp)) \
        .paginate(page, BLOGPOSTS_PER_PAGE, False).items = BlogPost.query.order_by(
        desc(BlogPost.timestamp)).paginate(page, BLOGPOSTS_PER_PAGE, False).items

    #c = CodeProject.query.order_by(desc(CodeProject.timestamp)) \
    #   .paginate(page, CODEPROJECTS_PER_PAGE, False).items = CodeProject.query.order_by(
    #    desc(CodeProject.timestamp)).paginate(page, CODEPROJECTS_PER_PAGE, False).items

    #url = url_for('blog_post', blog_title=blog[0].title_no_spaces)
    return render_template('blog.html',
                           blog_posts=b,
                           main_blog=main)
    #return redirect('blog_post',b.title_no_spaces) # figure out how I am supposed to pass this argument

# Figure out how to allow multiple different of these pages to trigger different things
@app.route('/blog_post/<blog_title>', methods=['GET', 'POST'])
def blog_post(blog_title):
    # Make a default title (most recent one)
    blog_title = blog_title.lower()

    b = BlogPost.query.filter_by(title_no_spaces=blog_title).first() #should grab first blog post to match title
    if b is None:
        return redirect('index')
    #c = [Comment(author='Steve',text="What a blog!"),Comment(author='Jason',text="Bash scripting is not useful")] #fake comments list
    c = Comment.query.filter_by(blogpost_id=b.id) # should grab all the comments on this post
    form = CommentForm()
    if form.validate_on_submit():
        flash('Comment Recieved') # Currently does not show
        return redirect('/blog_post')
    return render_template('blog_post.html',
                           blog_post=b,
                           comments=c,
                           form=form)


@app.route('/code_projects')
@app.route('/code_projects_list')
@app.route('/code_projects/<int:page>')
@app.route('/code_projects_list/<int:page>')
def code_projects_list(page=1):
    # For sidebar
    b = BlogPost.query.order_by(desc(BlogPost.timestamp)).limit(5).all()
    c = CodeProject.query.order_by(desc(CodeProject.timestamp))\
        .paginate(page, CODEPROJECTS_PER_PAGE, False).itemsc = CodeProject.query.order_by(desc(CodeProject.timestamp)).paginate(page, CODEPROJECTS_PER_PAGE, False).items
    #c = CodeProject.query.order_by(desc(CodeProject.timestamp)).all()
    return render_template('code_projects_list.html',
                           code_projects = c,
                           blog_posts = b)
"""
# I thought I was gonna have an individual page for each project, but I think I am going to end up keeping it in list form. At least for now.
@app.route('/')
@app.route('/code_project/<code_project_name_no_spaces>')
def code_project(code_project_name_no_spaces):
    return render_template('code_project.html')
"""
# for debugging. Never to be used publicly, lol
@app.route('/comment', methods=['GET', 'POST'])
def comment():
    form = CommentForm()
    return render_template('comment.html',
                           form=form)

# Error Handling!
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500